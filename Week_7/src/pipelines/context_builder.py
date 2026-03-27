from src.retriever.hybrid_retriever import hybrid_search
from src.retriever.reranker import rerank

def build_context(query, top_k=5):
    candidates   = hybrid_search(query, top_k=10)
    final_chunks = rerank(query, candidates, top_k=top_k)

    # deduplicate by page
    seen  = set()
    deduped = []
    for chunk in final_chunks:
        key = (chunk["metadata"]["source"], chunk["metadata"]["page"])
        if key not in seen:
            deduped.append(chunk)
            seen.add(key)

    # format for LLM
    parts = []
    for i, chunk in enumerate(deduped):
        source = chunk["metadata"]["source"].split("/")[-1]
        page   = chunk["metadata"]["page"]
        parts.append(f"[Source {i+1}: {source}, page {page}]\n{chunk['text']}")

    return {
        "query":      query,
        "context":    "\n\n".join(parts),
        "sources":    [{"source": c["metadata"]["source"],
                        "page":   c["metadata"]["page"],
                        "score":  c["rerank_score"]} for c in deduped],
        "num_chunks": len(deduped)
    }

if __name__ == "__main__":
    result = build_context("What are Crombie's pension benefits?")
    print(f"Built context from {result['num_chunks']} chunks\n")
    print("Sources:")
    for s in result["sources"]:
        print(f"  - {s['source'].split('/')[-1]} p.{s['page']} (score: {s['score']})")
    print("\n--- Context ---")
    print(result["context"][:800])