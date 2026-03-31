import faiss
import os
import numpy as np
import json
from src.embeddings.embedder import embed_single

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "src", "vectorstore")

# load once at module level
try:
    index = faiss.read_index(f"{VECTORSTORE_DIR}/index.faiss")
except:
    index = None

try:
    with open(f"{VECTORSTORE_DIR}/store.json") as f:
        store = json.load(f)
        texts = store["texts"]
        metadatas = store["metadatas"]
except:
    texts = []
    metadatas = []

try:
    print(f"QueryEngine ready — {index.ntotal} vectors loaded")
except:
    print("QueryEngine ready — no index loaded")

def search(query, top_k=5):
    try:
        query_vector = np.array([embed_single(query)], dtype=np.float32)
    except:
        return []

    results = []
    try:
        if index is not None:
            distances, indices = index.search(query_vector, top_k)
            for dist, idx in zip(distances[0], indices[0]):
                if idx == -1:
                    continue
                results.append({
                    "text":     texts[idx],
                    "metadata": metadatas[idx],
                    "score":    round(float(1 / (1 + dist)), 4)
                })
    except:
        pass

    return results

if __name__ == "__main__":
    try:
        results = search("What are the tasks for Day 2 feature engineering?")
        for r in results:
            print(f"[Score: {r['score']}] {r['metadata']['source']} p.{r['metadata']['page']}")
            print(r["text"][:200])
            print("---")
    except:
        pass