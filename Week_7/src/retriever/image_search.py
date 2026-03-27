import faiss
import numpy as np
import json
import os
from src.embeddings.clip_embedder import embed_text, embed_image

VECTORSTORE_DIR = "src/vectorstore"

# load index and store once at module level
index = faiss.read_index(f"{VECTORSTORE_DIR}/image_index.faiss")
with open(f"{VECTORSTORE_DIR}/image_store.json") as f:
    store = json.load(f)
texts     = store["texts"]
metadatas = store["metadatas"]
print(f"ImageSearcher ready. {index.ntotal} images indexed.")

def search_by_text(query, top_k=3):
    query_vector    = np.array([embed_text(query)], dtype=np.float32)
    scores, indices = index.search(query_vector, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "filename":   metadatas[idx]["filename"],
            "image_path": metadatas[idx]["image_path"],
            "caption":    metadatas[idx]["caption"],
            "ocr_text":   metadatas[idx]["ocr_text"],
            "score":      round(float(score), 4)
        })
    return results

def search_by_image(image_path, top_k=3):
    image_vector    = np.array([embed_image(image_path)], dtype=np.float32)
    scores, indices = index.search(image_vector, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "filename":   metadatas[idx]["filename"],
            "image_path": metadatas[idx]["image_path"],
            "caption":    metadatas[idx]["caption"],
            "score":      round(float(score), 4)
        })
    return results


if __name__ == "__main__":
    print("\n--- Text to Image search ---")
    results = search_by_text("boxer dog puppy", top_k=3)
    for r in results:
        print(f"[Score: {r['score']}] {r['filename']}")
        print(f"  Caption: {r['caption']}")
        print(f"  OCR: {r['ocr_text'][:100]}")
        print("---")

    print("\n--- Image to Image search ---")
    query_image = "src/data/images/german_shepheard.jpeg"
    if os.path.exists(query_image):
        results = search_by_image(query_image, top_k=3)
        for r in results:
            print(f"[Score: {r['score']}] {r['filename']}")
            print(f"  Caption: {r['caption']}")
            print("---")
    else:
        print("Query image not found — run image_ingest.py first")