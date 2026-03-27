# How to Run — Day 1 to Day 3

A complete step-by-step guide to set up and run the Enterprise Knowledge Intelligence System from scratch.

---

## Prerequisites

- Python 3.10 or higher
- Ubuntu / Linux (for Tesseract and Poppler)
- An Anthropic / OpenAI / Gemini API key
- At least 4GB RAM (for BLIP and CLIP models)

---

## Step 1 — Clone and Set Up the Project

```bash
# Create project folder
mkdir Week_7 && cd Week_7

# Create virtual environment
python -m venv venv_rag
source venv_rag/bin/activate

# Create the folder structure
mkdir -p src/{data/{raw,images,images/temp_pdf_pages},embeddings,pipelines,retriever,vectorstore,config,logs,evaluation,memory,generator}

# Create empty __init__.py files so Python treats folders as modules
touch src/__init__.py
touch src/embeddings/__init__.py
touch src/pipelines/__init__.py
touch src/retriever/__init__.py
```

---

## Step 2 — Install Dependencies

```bash
# Core RAG dependencies
pip install langchain langchain-anthropic langchain-community
pip install faiss-cpu numpy
pip install sentence-transformers
pip install pypdf python-docx docx2txt
pip install rank_bm25
pip install chromadb tiktoken

# Image RAG dependencies
pip install transformers torch pillow
pip install pytesseract pdf2image

# System dependencies (Ubuntu)
sudo apt install tesseract-ocr
sudo apt install poppler-utils
```

---

## Step 3 — Set Up Config

Create `src/config/model.yaml`:

```yaml
provider: anthropic
model_name: claude-haiku-4-5-20251001
api_key_env: ANTHROPIC_API_KEY
embedding_model: all-MiniLM-L6-v2
chunk_size: 600
chunk_overlap: 100
```

Set your API key:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Step 4 — Add Your Documents

```bash
# Add PDFs, DOCX, CSV or TXT files here
cp your_documents/* src/data/raw/

# Add images (PNG, JPG) or scanned PDFs here
cp your_images/* src/data/images/
```

Supported formats:

| Folder | Formats |
|---|---|
| `src/data/raw/` | PDF, DOCX, CSV, TXT |
| `src/data/images/` | PNG, JPG, JPEG, WEBP, scanned PDFs |

---

## DAY 1 — Text Ingestion and Basic Retrieval

### What Day 1 builds
Loads your documents → chunks them → generates embeddings → stores in FAISS → enables basic semantic search.

### Run ingestion

```bash
python -m src.pipelines.ingest
```

Expected output:
```
Loaded: your_document.pdf (134 pages/rows) [.pdf]
Loaded: customers.csv (10000 pages/rows) [.csv]
Created 10953 chunks from 10134 documents/pages
Embedder loaded: all-MiniLM-L6-v2
Batches: 100%|████| 343/343 [02:22<00:00]
Stored batch 1: chunks 0 to 5000
Stored batch 2: chunks 5000 to 10953
Done — 10953 chunks saved
```

Two files will be created:
- `src/vectorstore/index.faiss` — the vector index
- `src/vectorstore/store.json` — texts and metadata

### Test basic retrieval

```bash
python -m src.retriever.query_engine
```

Expected output:
```
QueryEngine ready — 10953 vectors loaded
[Score: 0.57] your_document.pdf p.115
...
```

✅ Day 1 complete when you see scored results printed.

---

## DAY 2 — Hybrid Retrieval + Reranking

### What Day 2 builds
Adds BM25 keyword search on top of semantic search → blends scores → reranks with a cross-encoder → builds clean context for the LLM.

### Install Day 2 dependency

```bash
pip install rank_bm25
```

### Test hybrid retriever

```bash
python -m src.retriever.hybrid_retriever
```

Expected output:
```
Building BM25 index...
BM25 ready — 10953 chunks indexed
[Hybrid: 0.74 | Sem: 0.57 | BM25: 1.0]
Source: your_document.pdf p.115
...
```

### Test reranker

```bash
python -m src.retriever.reranker
```

Expected output:
```
Reranker loaded
--- Reranked results ---
[Rerank: 7.36 | Hybrid: 0.74]
Source: your_document.pdf p.115
...
```

Note: The order of results may change after reranking — that means it is working correctly.

### Test full context builder

```bash
python -m src.pipelines.context_builder
```

Expected output:
```
Built context from 3 chunks

Sources used:
  - your_document.pdf p.115 (score: 7.36)
  - your_document.pdf p.116 (score: 5.07)
  - your_document.pdf p.99  (score: 4.93)

--- Context passed to LLM ---
[Source 1: your_document.pdf, page 115]
...
```

✅ Day 2 complete when you see hybrid scores, rerank scores, and a formatted context string.

---

## DAY 3 — Image RAG (Multimodal)

### What Day 3 builds
Ingests images using OCR + BLIP captions + CLIP embeddings → stores in a separate FAISS index → enables text-to-image and image-to-image search.

### Install Day 3 dependencies

```bash
pip install transformers torch pillow pytesseract pdf2image
sudo apt install tesseract-ocr poppler-utils
```

### Test CLIP embedder

```bash
python -m src.embeddings.clip_embedder
```

Expected output:
```
CLIP model loaded: openai/clip-vit-base-patch32
Text embedding dim: 512
Image embedding dim: 512
Dimensions match: True
```

⚠️ Both dimensions must be 512 and must match before continuing.

### Ingest images

```bash
python -m src.pipelines.image_ingest
```

Expected output:
```
CLIP model loaded: openai/clip-vit-base-patch32
Loading BLIP captioning model...
BLIP model loaded.
Converting scanned PDF: Dog-Pictures.pdf
  Converted page 1/1
Found 3 images. Processing...

[1/3] Internet_Speed.png
  OCR: DOWNLOAD Mbps 48.84...
  Caption: the settings of the game

[2/3] correlation_matrix.png
  OCR: Glucose BloodPressure BMI...
  Caption: a graph showing the number of people

[3/3] Dog-Pictures_page1.png
  OCR: Dog Pictures
  Caption: a bunch of dogs that are all different

Stored 3 images in FAISS
File types ingested: {'png': 2, 'scanned_pdf_page': 1}
```

Two new files will be created:
- `src/vectorstore/image_index.faiss`
- `src/vectorstore/image_store.json`

### Test image search

```bash
python -m src.retriever.image_search
```

Expected output:
```
ImageSearcher ready. 3 images indexed.

--- Text to Image search ---
[Score: 0.29] Dog-Pictures_page1.png
  Caption: a bunch of dogs that are all different
  OCR: Dog Pictures
---

--- Image to Image search ---
[Score: 1.0] pupp_image.jpeg
  Caption: a small dog sitting on the ground
---
[Score: 0.76] Dog-Pictures_page1.png
  Caption: a bunch of dogs that are all different
---
```

✅ Day 3 complete when text search returns relevant images with scores and image-to-image search returns similar images.

---

## Final Folder Structure After Day 1 to Day 3

```
src/
├── config/
│   └── model.yaml
├── data/
│   ├── raw/                        ← your PDFs, DOCX, CSV, TXT
│   └── images/                     ← your PNG, JPG, scanned PDFs
│       └── temp_pdf_pages/         ← auto-created PDF page PNGs
├── embeddings/
│   ├── embedder.py                 ← MiniLM text embedder
│   └── clip_embedder.py            ← CLIP image + text embedder
├── pipelines/
│   ├── ingest.py                   ← Day 1 text ingestion
│   ├── image_ingest.py             ← Day 3 image ingestion
│   └── context_builder.py          ← Day 2 context formatter
├── retriever/
│   ├── query_engine.py             ← Day 1 basic search
│   ├── hybrid_retriever.py         ← Day 2 BM25 + semantic
│   ├── reranker.py                 ← Day 2 cross-encoder
│   └── image_search.py             ← Day 3 image search
└── vectorstore/
    ├── index.faiss                 ← text vectors
    ├── store.json                  ← text metadata
    ├── image_index.faiss           ← image vectors
    └── image_store.json            ← image metadata
```

---

## Common Errors and Fixes

| Error | Fix |
|---|---|
| `No module named src` | Run commands from the `Week_7/` root folder |
| `tesseract is not installed` | Run `sudo apt install tesseract-ocr` |
| `poppler not found` | Run `sudo apt install poppler-utils` |
| `Collection not found` | Run `ingest.py` before `query_engine.py` |
| `Batch size greater than 5461` | Already handled — batches of 5000 |
| `Dimensions don't match` | Delete image FAISS files and re-run `image_ingest.py` |
| `UNEXPECTED position_ids` | Safe to ignore — harmless warning |
| `HF Hub unauthenticated` | Safe to ignore — models still download fine |

---

## Quick Reference — Run Order

```
Day 1:
  python -m src.pipelines.ingest
  python -m src.retriever.query_engine

Day 2:
  python -m src.retriever.hybrid_retriever
  python -m src.retriever.reranker
  python -m src.pipelines.context_builder

Day 3:
  python -m src.embeddings.clip_embedder
  python -m src.pipelines.image_ingest
  python -m src.retriever.image_search
```