# RAG Architecture — Day 1

## Overview

This document describes the ingestion and retrieval architecture built on Day 1 of the Enterprise Knowledge Intelligence System. The system enables question answering over internal documents (PDFs, DOCX, TXT) using Retrieval-Augmented Generation (RAG).

---

## What is RAG?

RAG stands for Retrieval-Augmented Generation. Instead of asking an LLM to answer from memory (which causes hallucination), RAG first retrieves relevant passages from your own documents, then passes those passages to the LLM as context. The LLM only answers based on what was retrieved.

```
User Question → Retriever → Relevant Chunks → LLM → Grounded Answer
```

---

## System Components

### 1. Document Loader (`pipelines/ingest.py`)

Loads raw files from `src/data/raw/` using LangChain loaders.

| File Type | Loader Used |
|-----------|-------------|
| `.pdf` | `PyPDFLoader` |
| `.docx` | `Docx2txtLoader` |
| `.txt` | `TextLoader` |

Each loader returns a list of `Document` objects containing raw text and basic metadata (source path, page number).

### 2. Text Splitter (`pipelines/ingest.py`)

Uses `RecursiveCharacterTextSplitter` to break documents into chunks.

| Parameter | Value | Reason |
|-----------|-------|--------|
| `chunk_size` | 600 tokens | Fits within LLM context with room for multiple chunks |
| `chunk_overlap` | 100 tokens | Prevents losing context at chunk boundaries |
| `separators` | `\n\n`, `\n`, `.`, ` ` | Splits on natural language boundaries first |

A chunk is the atomic unit of retrieval — the smallest piece of text the system can return as context.

### 3. Metadata Tagger (`pipelines/ingest.py`)

Each chunk is tagged with metadata before storage. This enables filtered search later.

```python
{
  "chunk_id": "chunk_42",
  "source": "employee_handbook.pdf",
  "page": 7,
  "tags": "enterprise_doc"
}
```

### 4. Embedder (`embeddings/embedder.py`)

Converts text chunks into dense vector representations using `sentence-transformers/all-MiniLM-L6-v2`.

- Model runs **locally** — no API calls needed for embedding
- Output: 384-dimensional float vector per chunk
- Similar meaning → similar vectors → close distance in vector space

### 5. Vector Store (`src/vectorstore/`)

Stores all chunk vectors in a **Faiss** persistent database.

- Persisted to disk at `src/vectorstore/`
- Supports similarity search by cosine distance

### 6. Query Engine (`retriever/query_engine.py`)

At query time, the user's question is embedded using the same model, then ChromaDB finds the `top_k` most similar chunk vectors.

```
Query → Embed query → ChromaDB similarity search → Top 5 chunks returned
```

Each result includes the chunk text, its metadata, and a relevance score (0 to 1, higher is better).

---

## Data Flow

```
src/data/raw/
    ├── document.pdf
    ├── policy.docx
    └── notes.txt
         │
         ▼
   [Document Loader]
   Reads raw files into Document objects
         │
         ▼
   [Text Splitter]
   Breaks into 500–800 token chunks with 100-token overlap
         │
         ▼
   [Metadata Tagger]
   Attaches source, page, chunk_id, tags
         │
         ▼
   [Embedder]
   Converts each chunk to a 384-dim vector (local model)
         │
         ▼
   [ChromaDB]
   Persists vectors + text + metadata to disk
         │
         ▼ (at query time)
   [Query Engine]
   Embeds user question → similarity search → returns top 5 chunks
```

---

## File Structure

```
src/
├── config/
│   └── model.yaml              # Provider, model, chunk settings
├── data/
│   └── raw/                    # Place your PDFs, DOCX, TXT files here
├── embeddings/
│   └── embedder.py             # Embedding model wrapper
├── pipelines/
│   └── ingest.py               # Full ingestion pipeline
├── retriever/
│   └── query_engine.py         # Similarity search engine
└── vectorstore/                
```

---

## How to Run

```bash
# Install dependencies
pip install langchain langchain-anthropic langchain-community faiss-cpu tiktoken pypdf python-docx sentence-transformers

# Set API key
export GROQ_AI_KEY="your-key-here"

# Add documents
cp your_documents/* src/data/raw/

# Run ingestion
cd src
python pipelines/ingest.py

# Test retrieval
python retriever/query_engine.py
```

---