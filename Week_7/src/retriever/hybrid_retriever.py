import faiss
import numpy as np
import json
from rank_bm25 import BM25Okapi
from src.embeddings.embedder import embed_single

VECTORSTORE_DIR = "src/vectorstore"

# load everything once at module level
index = faiss.read_index(f"{VECTORSTORE_DIR}/index.faiss")
with open(f"{VECTORSTORE_DIR}/store.json") as f:
    store = json.load(f)
texts     = store["texts"]
metadatas = store["metadatas"]
ids       = [m["chunk_id"] for m in metadatas]

# build BM25 index
print("Building BM25 index...")
tokenized_corpus = [t.lower().split() for t in texts]
bm25 = BM25Okapi(tokenized_corpus)
print(f"BM25 ready — {len(texts)} chunks indexed")

def semantic_search(query, top_k=10):
    query_vector = np.array([embed_single(query)], dtype=np.float32)
    distances, indices = index.search(query_vector, top_k)
    results = {}
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        results[ids[idx]] = {
            "text":           texts[idx],
            "metadata":       metadatas[idx],
            "semantic_score": round(float(1 / (1 + dist)), 4),
            "bm25_score":     0.0
        }
    return results

def bm25_search(query, top_k=10):
    scores      = bm25.get_scores(query.lower().split())
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    max_score   = scores[top_indices[0]] if scores[top_indices[0]] > 0 else 1
    results = {}
    for idx in top_indices:
        results[ids[idx]] = {
            "text":           texts[idx],
            "metadata":       metadatas[idx],
            "semantic_score": 0.0,
            "bm25_score":     round(scores[idx] / max_score, 4)
        }
    return results

def hybrid_search(query, top_k=5, semantic_weight=0.6, bm25_weight=0.4):
    sem_results  = semantic_search(query)
    bm25_results = bm25_search(query)
    all_ids      = set(sem_results.keys()) | set(bm25_results.keys())

    merged = {}
    for chunk_id in all_ids:
        sem  = sem_results.get(chunk_id, {})
        bm   = bm25_results.get(chunk_id, {})
        s    = sem.get("semantic_score", 0.0)
        b    = bm.get("bm25_score", 0.0)
        merged[chunk_id] = {
            "text":           sem.get("text") or bm.get("text"),
            "metadata":       sem.get("metadata") or bm.get("metadata"),
            "semantic_score": round(s, 4),
            "bm25_score":     round(b, 4),
            "hybrid_score":   round((semantic_weight * s) + (bm25_weight * b), 4)
        }

    ranked = sorted(merged.values(), key=lambda x: x["hybrid_score"], reverse=True)
    return ranked[:top_k]

if __name__ == "__main__":
    results = hybrid_search("How much minimum internet speed for work from home")
    for r in results:
        print(f"[Hybrid: {r['hybrid_score']} | Sem: {r['semantic_score']} | BM25: {r['bm25_score']}]")
        print(f"Source: {r['metadata']['source']} p.{r['metadata']['page']}")
        print(r["text"][:200])
        print("---")