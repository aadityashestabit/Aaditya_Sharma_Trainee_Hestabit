import faiss
import numpy as np
import json
from src.embeddings.embedder import embed_single

VECTORSTORE_DIR = "src/vectorstore"

# load once at module level
index = faiss.read_index(f"{VECTORSTORE_DIR}/index.faiss")
with open(f"{VECTORSTORE_DIR}/store.json") as f:
    store = json.load(f)
    texts = store["texts"]
    metadatas = store["metadatas"]
print(f"QueryEngine ready — {index.ntotal} vectors loaded")

def search(query, top_k=5):
    query_vector = np.array([embed_single(query)], dtype=np.float32)
    distances, indices = index.search(query_vector, top_k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "text":     texts[idx],
            "metadata": metadatas[idx],
            "score":    round(float(1 / (1 + dist)), 4)
        })
    return results

if __name__ == "__main__":
    results = search("How much minimum internet speed for work from home")
    for r in results:
        print(f"[Score: {r['score']}] {r['metadata']['source']} p.{r['metadata']['page']}")
        print(r["text"][:200])
        print("---")