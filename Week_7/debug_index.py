"""
Run this from your project ROOT directory:
    python debug_index.py

It tells you exactly what's inside your FAISS index and whether
text ↔ image embeddings are actually compatible.
"""

import faiss
import numpy as np
import json
import os
import torch
from PIL import Image

# ── locate files ──────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "src", "vectorstore")
IMAGE_DIR       = os.path.join(BASE_DIR, "src", "data", "images")

index_path = os.path.join(VECTORSTORE_DIR, "image_index.faiss")
store_path = os.path.join(VECTORSTORE_DIR, "image_store.json")

print("=" * 60)
print("STEP 1 — FAISS index file")
print("=" * 60)

if not os.path.exists(index_path):
    print("❌ image_index.faiss NOT FOUND — ingest hasn't run or path is wrong")
    print(f"   Expected: {index_path}")
else:
    mtime = os.path.getmtime(index_path)
    import datetime
    print(f"✅ Found: {index_path}")
    print(f"   Last modified : {datetime.datetime.fromtimestamp(mtime)}")
    print(f"   File size     : {os.path.getsize(index_path):,} bytes")

    index = faiss.read_index(index_path)
    print(f"   Vectors stored: {index.ntotal}")
    print(f"   Dimension     : {index.d}")
    print()

    if index.d != 512:
        print(f"🚨 DIMENSION MISMATCH: index has dim={index.d} but CLIP outputs 512-dim vectors.")
        print(f"   This means the index was built with a DIFFERENT embedder (e.g. SentenceTransformer=384).")
        print(f"   → DELETE image_index.faiss and re-run ingest.\n")
    else:
        print(f"✅ Dimension is 512 — matches CLIP vit-base-patch32\n")

    # Check norms of stored vectors
    print("=" * 60)
    print("STEP 2 — Stored vector norms (should all be ~1.0 for cosine sim)")
    print("=" * 60)
    norms = []
    for i in range(min(index.ntotal, 10)):
        vec = np.zeros((index.d,), dtype=np.float32)
        index.reconstruct(i, vec)
        norms.append(np.linalg.norm(vec))
    print(f"   Norms of first {len(norms)} vectors: {[round(n,4) for n in norms]}")
    if any(abs(n - 1.0) > 0.01 for n in norms):
        print("🚨 Norms are NOT ~1.0 — vectors were stored without L2 normalization.")
        print("   IndexFlatIP dot product ≠ cosine similarity in this case.")
        print("   → Re-run ingest with the fixed image_ingest.py\n")
    else:
        print("✅ All norms ~1.0 — vectors are properly normalized\n")

print("=" * 60)
print("STEP 3 — Live embedding comparison")
print("=" * 60)

try:
    from src.embeddings.clip_embedder import embed_text, embed_image

    # Text embedding
    text_vec = np.array(embed_text("a dog"), dtype=np.float32)
    print(f"embed_text output  — dim: {len(text_vec)}, norm: {np.linalg.norm(text_vec):.4f}")

    # Find a real image to test with
    test_image = None
    for ext in ["*.jpg", "*.jpeg", "*.png"]:
        from pathlib import Path
        imgs = list(Path(IMAGE_DIR).glob(ext))
        if imgs:
            test_image = str(imgs[0])
            break

    if test_image:
        img_vec = np.array(embed_image(test_image), dtype=np.float32)
        print(f"embed_image output — dim: {len(img_vec)}, norm: {np.linalg.norm(img_vec):.4f}")
        print(f"Image used: {os.path.basename(test_image)}")

        if len(text_vec) == len(img_vec) == 512:
            score = float(np.dot(text_vec, img_vec))
            print(f"\nLive cosine similarity (text='a dog' vs first image): {score:.4f}")
            if score < 0.15:
                print("🚨 Score is extremely low — embeddings may be in different spaces")
            elif score < 0.25:
                print("⚠️  Score is low — image content may genuinely not match 'a dog'")
            else:
                print("✅ Score looks reasonable for CLIP")
        else:
            print(f"🚨 Dimension mismatch: text={len(text_vec)}, image={len(img_vec)}")
    else:
        print("⚠️  No images found in IMAGE_DIR to test embed_image()")

except Exception as e:
    print(f"❌ Embedding test failed: {e}")

print()
print("=" * 60)
print("STEP 4 — image_store.json metadata check")
print("=" * 60)

if os.path.exists(store_path):
    with open(store_path) as f:
        store = json.load(f)
    metadatas = store.get("metadatas", [])
    print(f"   Entries in store : {len(metadatas)}")
    for i, m in enumerate(metadatas[:3]):
        print(f"\n   [{i}] {os.path.basename(m.get('image_path','?'))}")
        print(f"        caption : {m.get('caption','')}")
        print(f"        ocr     : {m.get('ocr_text','')[:80]!r}")
    if len(metadatas) != (index.ntotal if os.path.exists(index_path) else -1):
        print("\n🚨 MISMATCH: store has different count than FAISS index!")
        print("   → Stale index from a previous ingest. Delete both files and re-ingest.")
else:
    print("❌ image_store.json NOT FOUND")

print()
print("=" * 60)
print("STEP 5 — Direct search test (bypass MIN_SCORE)")
print("=" * 60)

try:
    from src.embeddings.clip_embedder import embed_text
    index = faiss.read_index(index_path)
    with open(store_path) as f:
        store = json.load(f)

    query = "document"
    q_vec = np.array([embed_text(query)], dtype=np.float32)
    faiss.normalize_L2(q_vec)  # ensure normalized

    scores, indices = index.search(q_vec, min(5, index.ntotal))
    print(f"Query: '{query}'")
    print(f"Top results (no threshold filter):")
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        meta = store["metadatas"][idx]
        print(f"   score={score:.4f}  file={os.path.basename(meta['image_path'])}")
        print(f"           caption={meta['caption']}")
except Exception as e:
    print(f"❌ Direct search failed: {e}")