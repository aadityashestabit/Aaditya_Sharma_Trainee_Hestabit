# Multimodal RAG — Day 3

## What is Image RAG?

Normal RAG only searches text. Image RAG extends this to images — diagrams, charts, screenshots, scanned forms. You can ask a question in plain text and the system finds the most relevant image from your collection. The secret is CLIP, a model that understands both text and images in the same vector space.

---

## The Full Pipeline

```
                        ┌─────────────────────────────────────────┐
                        │           INGESTION (run once)          │
                        └─────────────────────────────────────────┘

  Image (PNG/JPG)
       │
       ├─────────────────────────────────────────────┐
       │                                             │
       ▼                                             ▼
  ┌─────────┐                                   ┌─────────┐
  │Tesseract│                                   │  BLIP   │
  │  OCR    │                                   │ Caption │
  └────┬────┘                                   └────┬────┘
       │ extracted text                              │ generated caption
       └──────────────┬──────────────────────────────┘
                      │ combined text
                      │ "Caption: a bar chart\nOCR: Revenue 2022..."
                      ▼
              ┌───────────────┐
              │ CLIP Embedder │  ← also embeds the image visually
              │  (512-dim)    │
              └───────┬───────┘
                      │ 512-dim vector
                      ▼
              ┌───────────────┐
              │  FAISS Index  │  image_index.faiss
              │  + JSON store │  image_store.json
              └───────────────┘


                        ┌─────────────────────────────────────────┐
                        │           SEARCH (run anytime)          │
                        └─────────────────────────────────────────┘

  Text query
  "correlation matrix heatmap"
       │
       ▼
  ┌───────────────┐
  │ CLIP Embedder │  converts text to same 512-dim space as images
  └───────┬───────┘
          │ 512-dim vector
          ▼
  ┌───────────────┐
  │  FAISS Search │  finds closest image vectors
  └───────┬───────┘
          │ top-k results with scores
          ▼
  ┌───────────────────────────────────┐
  │  Results                          │
  │  [Score: 0.61] correlation.png    │
  │    Caption: a heatmap chart       │
  │    OCR: Glucose BloodPressure ... │
  └───────────────────────────────────┘
```

---

## The Three Tools

### Tesseract OCR
Extracts any text printed on an image — numbers, labels, titles, axis names. Works best on clean screenshots and charts. Noisy or handwritten images may produce garbled output, which is fine — CLIP handles those visually anyway.

### BLIP Captioning
Generates a natural language description of what the image looks like. The base model (`blip-image-captioning-base`) is not always accurate for UI screenshots but gives useful descriptions for photographs and diagrams. The caption is stored alongside OCR text to make search richer.

### CLIP Embedder
The core of Image RAG. CLIP maps both images and text into the same 512-dimensional vector space — meaning "a heatmap chart" and an actual heatmap image will end up close together in that space. This is what makes text-to-image search possible.

---

## Why FAISS IndexFlatIP?

We use `IndexFlatIP` (inner product) for images instead of `IndexFlatL2` (L2 distance) used for text chunks. CLIP vectors are normalized to unit length, so inner product equals cosine similarity directly. Higher score = more similar. No conversion needed.

| Index type | Used for | Score meaning |
|---|---|---|
| `IndexFlatL2` | Text chunks | Lower = better (distance) |
| `IndexFlatIP` | Images | Higher = better (similarity) |

---

## Files

```
src/
├── embeddings/
│   └── clip_embedder.py       # CLIP text + image → 512-dim vectors
├── pipelines/
│   └── image_ingest.py        # OCR + caption + CLIP → FAISS
├── retriever/
│   └── image_search.py        # text query → similar images
└── vectorstore/
    ├── image_index.faiss       # CLIP vectors (512-dim)
    └── image_store.json        # captions, OCR text, file paths
```

---


## Real Test Result

Image: `correlation_matrix.png` (diabetes dataset heatmap)

| Query | Score |
|---|---|
| `"correlation matrix heatmap"` | 0.29 |
| `"glucose blood pressure BMI diabetes"` | best match |
| `"download speed"` | 0.28 (unrelated — low score expected) |

OCR correctly extracted: `Glucose`, `BloodPressure`, `BMI`, `PedigreeFunction`, `Age`, `Outcome` — all column names from the heatmap.

---

