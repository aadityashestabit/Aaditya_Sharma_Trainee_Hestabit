from sentence_transformers import CrossEncoder
from src.retriever.hybrid_retriever import hybrid_search

# load once at module level
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
print("Reranker loaded")

def rerank(query, chunks, top_k=5):
    pairs  = [(query, chunk["text"]) for chunk in chunks]
    scores = model.predict(pairs)
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = round(float(score), 4)
    return sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)[:top_k]

if __name__ == "__main__":
    candidates = hybrid_search("How much minimum internet speed for work from home", top_k=10)
    final      = rerank("How much minimum internet speed for work from home", candidates)
    print("\n--- Reranked results ---")
    for r in final:
        print(f"[Rerank: {r['rerank_score']} | Hybrid: {r['hybrid_score']}]")
        print(f"Source: {r['metadata']['source']} p.{r['metadata']['page']}")
        print(r["text"][:200])
        print("---")