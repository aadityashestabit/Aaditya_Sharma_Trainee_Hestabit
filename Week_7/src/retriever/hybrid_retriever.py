import faiss
import numpy as np
import json
import os
from rank_bm25 import BM25Okapi
from src.embeddings.embedder import embed_single

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "src", "vectorstore")

# load main text index (Day 1 ingest) 
try:
    index_main = faiss.read_index(f"{VECTORSTORE_DIR}/index.faiss")
except:
    index_main = None

try:
    with open(f"{VECTORSTORE_DIR}/store.json") as f:
        store_main = json.load(f)
except:
    store_main = {"texts": [], "metadatas": []}

#  load image pipeline text index (image_ingest.py) 
index_img_text = None
store_img_text = {"texts": [], "metadatas": []}

img_text_index_path = f"{VECTORSTORE_DIR}/text_index.faiss"
img_text_store_path = f"{VECTORSTORE_DIR}/text_store.json"

# load image text and metadata 
try:
    if os.path.exists(img_text_index_path) and os.path.exists(img_text_store_path):
        index_img_text = faiss.read_index(img_text_index_path)
        with open(img_text_store_path) as f:
            store_img_text = json.load(f)
        print(f"Image text index loaded — {index_img_text.ntotal} chunks")
    else:
        print("No image text index found — skipping")
except:
    index_img_text = None
    store_img_text = {"texts": [], "metadatas": []}

# combine both stores - list concetanation 
all_texts     = store_main["texts"]     + store_img_text["texts"]
all_metadatas = store_main["metadatas"] + store_img_text["metadatas"]

try:
    all_ids = [m["chunk_id"] for m in store_main["metadatas"]] + \
              [f"img_text_{i}" for i in range(len(store_img_text["texts"]))]
              
              # unique chunk ids created for text - chunk x -- for image text - img_text_x
except:
    all_ids = []

#  build BM25 over combined corpus 
try:
    print(f"Building BM25 index over {len(all_texts)} chunks...")
    bm25 = BM25Okapi([t.lower().split() for t in all_texts])
    print("BM25 ready.")
except:
    bm25 = None

# semantic search 
def semantic_search(query, top_k=10):
    try:
        query_vector = np.array([embed_single(query)], dtype=np.float32)
    except:
        return {}

    results = {}

    try:
        if index_main is not None:
            distances, indices = index_main.search(query_vector, top_k)
            for dist, idx in zip(distances[0], indices[0]):
                if idx == -1:
                    continue
                chunk_id = all_ids[idx]
                results[chunk_id] = {
                    "text":           all_texts[idx],
                    "metadata":       all_metadatas[idx],
                    "semantic_score": round(float(1 / (1 + dist)), 4),
                    "bm25_score":     0.0
                }
    except:
        pass

    try:
        if index_img_text is not None:
            offset             = len(store_main["texts"])
            distances, indices = index_img_text.search(query_vector, top_k)
            for dist, idx in zip(distances[0], indices[0]):
                if idx == -1:
                    continue
                combined_idx = offset + idx
                chunk_id     = all_ids[combined_idx]
                results[chunk_id] = {
                    "text":           all_texts[combined_idx],
                    "metadata":       all_metadatas[combined_idx],
                    "semantic_score": round(float(1 / (1 + dist)), 4),
                    "bm25_score":     0.0
                }
    except:
        pass

    return results

def bm25_search(query, top_k=10):
    try:
        scores      = bm25.get_scores(query.lower().split())
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        max_score   = scores[top_indices[0]] if scores[top_indices[0]] > 0 else 1

        results = {}
        for idx in top_indices:
            chunk_id = all_ids[idx]
            results[chunk_id] = {
                "text":           all_texts[idx],
                "metadata":       all_metadatas[idx],
                "semantic_score": 0.0,
                "bm25_score":     round(scores[idx] / max_score, 4) # normalize bm25 score 0-1 
            }
        return results
    except:
        return {}

def hybrid_search(query, top_k=5, semantic_weight=0.6, bm25_weight=0.4):
    try:
        sem_results  = semantic_search(query) # run semantic search 
        bm25_results = bm25_search(query) # run bm 25 search

        all_chunk_ids = set(sem_results.keys()) | set(bm25_results.keys())  # | - union of semantic and bm25 chunks 

        merged = {}
        for chunk_id in all_chunk_ids:
            sem  = sem_results.get(chunk_id, {})  # empty dict if not in semantic results
            bm   = bm25_results.get(chunk_id, {})  # empty dict if not in BM25 results

            s = sem.get("semantic_score", 0.0) # 0.0 if not found 
            b = bm.get("bm25_score", 0.0)

            merged[chunk_id] = {
                "text":           sem.get("text") or bm.get("text"),
                "metadata":       sem.get("metadata") or bm.get("metadata"),
                "semantic_score": round(s, 4),
                "bm25_score":     round(b, 4),
                "hybrid_score":   round((semantic_weight * s) + (bm25_weight * b), 4) # (0.6 * semantic ) + (0.4 * bm25)
            }

        ranked = sorted(merged.values(), key=lambda x: x["hybrid_score"], reverse=True) # sort and return top 5 
        return ranked[:top_k]
    except:
        return []

if __name__ == "__main__":
    try:
        results = hybrid_search("What are the tasks for Day 2 feature engineering?")
        for r in results:
            print(f"[Hybrid: {r['hybrid_score']} | Sem: {r['semantic_score']} | BM25: {r['bm25_score']}]")
            print(f"Source: {r['metadata'].get('source', 'unknown')}")
            print(r["text"][:200])
            print("---")
    except:
        pass