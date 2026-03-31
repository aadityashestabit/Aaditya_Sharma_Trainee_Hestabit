from src.retriever.hybrid_retriever import hybrid_search
from src.retriever.reranker import rerank

from src.retriever.hybrid_retriever import hybrid_search
from src.retriever.reranker import rerank

def build_context(query, top_k=5):
    try:
        candidates   = hybrid_search(query, top_k=10)
        final_chunks = rerank(query, candidates, top_k=top_k)
    except:
        return {
            "query": query,
            "context": "",
            "sources": [],
            "num_chunks": 0
        }

    try:
        # filter negative scores but always keep at least 1 chunk
        positive = [c for c in final_chunks if c["rerank_score"] > 0]
        final_chunks = positive if positive else final_chunks[:1]
    except:
        pass

    try:
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
    except:
        deduped = final_chunks

    try:
        # format for LLM
        parts = []
        for i, chunk in enumerate(deduped):
            source = chunk["metadata"].get("source", "unknown").split("/")[-1]
            page   = chunk["metadata"].get("page", "")
            label  = f"Source {i+1}: {source}" + (f", page {page}" if page else "")
            parts.append(f"[{label}]\n{chunk['text']}")
    except:
        parts = []

    try:
        return {
            "query":      query,
            "context":    "\n\n".join(parts),
            "sources":    [{"source": c["metadata"].get("source", "unknown"),
                            "page":   c["metadata"].get("page", ""),
                            "score":  c["rerank_score"]} for c in deduped],
            "num_chunks": len(deduped)
        }
    except:
        return {
            "query": query,
            "context": "",
            "sources": [],
            "num_chunks": 0
        }

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "test query"
    print(build_context(query))