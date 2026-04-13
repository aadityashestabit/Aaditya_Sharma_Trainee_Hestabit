from src.retriever.hybrid_retriever import hybrid_search
from src.retriever.reranker import rerank

def build_context(query, top_k=5):
    
    # step 1 - hybrid search 
    candidates = hybrid_search(query, top_k=10)

    # step 2 - filter out CSV chunks — CSV data is for SQL RAG only 
    candidates = [
        c for c in candidates
        if not c["metadata"].get("source", "").endswith(".csv")
    ]

    if not candidates:
        return {
            "query":      query,
            "context":    "",
            "sources":    [],
            "num_chunks": 0
        }
        
    # step 3 - rerank 
    final_chunks = rerank(query, candidates, top_k=top_k)

    # keep positive scores but always keep at least 1
    positive     = [c for c in final_chunks if c["rerank_score"] > 0]
    final_chunks = positive if positive else final_chunks[:1]

    # deduplicate by source + page
    seen    = set()
    deduped = []
    for chunk in final_chunks:
        source = chunk["metadata"].get("source", "unknown")
        page   = chunk["metadata"].get("page", 0)
        key    = (source, page)
        if key not in seen:
            deduped.append(chunk)
            seen.add(key)

    # format for LLM
    parts = []
    for i, chunk in enumerate(deduped):
        source = chunk["metadata"].get("source", "unknown").split("/")[-1] # extract just the file name 
        page   = chunk["metadata"].get("page", "")
        label  = f"Source {i+1}: {source}" + (f", page {page}" if page else "") # source label [Source 1: Week-6-ML.pdf, page 2]
        parts.append(f"[{label}]\n{chunk['text']}")

    return {
        "query":      query, # original question 
        "context":    "\n\n".join(parts),  # formatted string for LLM system prompt 
        "sources":    [{"source": c["metadata"].get("source", "unknown"), # list of sources page score for ui 
                        "page":   c["metadata"].get("page", ""),
                        "score":  c["rerank_score"]} for c in deduped],
        "num_chunks": len(deduped) # how many chunks made it through 
    }

if __name__ == "__main__":
    import sys
    query  = sys.argv[1] if len(sys.argv) > 1 else "What is in the documents?"
    result = build_context(query)
    print(f"Built context from {result['num_chunks']} chunks")
    for s in result["sources"]:
        print(f"  - {s['source'].split('/')[-1]} p.{s['page']} (score: {s['score']})")
    print("\n--- Context ---")
    print(result["context"][:800])