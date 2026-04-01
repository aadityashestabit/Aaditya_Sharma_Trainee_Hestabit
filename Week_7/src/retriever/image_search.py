import faiss
import numpy as np
import json
import os
from src.embeddings.clip_embedder import embed_text, embed_image

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "src", "vectorstore")
MIN_SCORE_TEXT  = 0.2  # text→image needs lower threshold
MIN_SCORE_IMAGE = 0.5  # image→image can use higher threshold


# load image index
try:
    image_index = faiss.read_index(f"{VECTORSTORE_DIR}/image_index.faiss")
except:
    image_index = None

try:
    with open(f"{VECTORSTORE_DIR}/image_store.json") as f:
        image_store = json.load(f)
except:
    image_store = {"texts": [], "metadatas": []}

image_texts     = image_store["texts"]
image_metadatas = image_store["metadatas"]

try:
    print(f"ImageSearcher ready. {image_index.ntotal} images indexed.")
except:
    print("ImageSearcher ready. No index loaded.")

def search_by_text(query, top_k=3):
    try:
        query_vector = np.array([embed_text(query)], dtype=np.float32)
    except:
        return []

    results = []
    try:
        if image_index is not None:
            scores, indices = image_index.search(query_vector, top_k)
            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:
                    continue
                if score < MIN_SCORE_TEXT:
                    continue
                meta = image_metadatas[idx]
                results.append({
                    "filename":   os.path.basename(meta["image_path"]),
                    "image_path": meta["image_path"],
                    "caption":    meta["caption"],
                    "ocr_text":   meta.get("ocr_text", ""),
                    "score":      round(float(score), 4)
                })
    except:
        pass

    return results

def search_by_image(image_path, top_k=3):
    try:
        image_vector = np.array([embed_image(image_path)], dtype=np.float32)
    except:
        return []

    results = []
    try:
        if image_index is not None:
            scores, indices = image_index.search(image_vector, top_k)
            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:
                    continue
                if score < MIN_SCORE_IMAGE:
                    continue
                meta = image_metadatas[idx]
                results.append({
                    "filename":   os.path.basename(meta["image_path"]),
                    "image_path": meta["image_path"],
                    "caption":    meta["caption"],
                    "ocr_text":   meta.get("ocr_text", ""),
                    "score":      round(float(score), 4)
                })
    except:
        pass

    return results

if __name__ == "__main__":
    try:
        print("\n--- Text to Image search ---")
        results = search_by_text("dog breeds", top_k=3)
        for r in results:
            print(f"[Score: {r['score']}] {r['filename']}")
            print(f"  Caption: {r['caption']}")
            print("---")
    except:
        pass