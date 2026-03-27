from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, CSVLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import numpy as np
import json
import os
from src.embeddings.embedder import embed

RAW_DATA_DIR = "src/data/raw"
VECTORSTORE_DIR = "src/vectorstore"

def load_documents():
    docs = []
    supported = {".pdf", ".docx", ".csv", ".txt"}

    for filepath in Path(RAW_DATA_DIR).rglob("*"):
        ext = filepath.suffix.lower()
        if ext not in supported:
            continue
        try:
            if ext == ".pdf":
                loader = PyPDFLoader(str(filepath))
            elif ext == ".docx":
                loader = Docx2txtLoader(str(filepath))
            elif ext == ".txt":
                loader = TextLoader(str(filepath), encoding="utf-8")
            elif ext == ".csv":
                loader = CSVLoader(str(filepath), encoding="utf-8")
            loaded = loader.load()
            docs.extend(loaded)
            print(f"Loaded: {filepath.name} ({len(loaded)} pages/rows)")
        except Exception as e:
            print(f"Failed: {filepath.name} — {e}")
    return docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks")
    return chunks

def build_metadata(chunk, idx):
    meta = chunk.metadata.copy()
    meta["chunk_id"] = f"chunk_{idx}"
    meta["source"]   = meta.get("source", "unknown")
    meta["page"]     = meta.get("page", 0)
    meta["tags"]     = "enterprise_doc"
    source = meta["source"].lower()
    if source.endswith(".pdf"):   meta["file_type"] = "pdf"
    elif source.endswith(".docx"): meta["file_type"] = "docx"
    elif source.endswith(".csv"):  meta["file_type"] = "csv"
    elif source.endswith(".txt"):  meta["file_type"] = "txt"
    else:                          meta["file_type"] = "unknown"
    return meta

def ingest():
    docs      = load_documents()
    chunks    = chunk_documents(docs)
    texts     = [c.page_content for c in chunks]
    metadatas = [build_metadata(c, i) for i, c in enumerate(chunks)]

    # generate embeddings
    embeddings = embed(texts)
    vectors    = np.array(embeddings, dtype=np.float32)

    # build and save FAISS index
    index = faiss.IndexFlatL2(vectors.shape[1])
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    BATCH_SIZE = 5000
    for i in range(0, len(vectors), BATCH_SIZE):
        index.add(vectors[i:i+BATCH_SIZE])
        print(f"Stored batch {i//BATCH_SIZE + 1}")

    faiss.write_index(index, f"{VECTORSTORE_DIR}/index.faiss")

    with open(f"{VECTORSTORE_DIR}/store.json", "w") as f:
        json.dump({"texts": texts, "metadatas": metadatas}, f)

    print(f"Done — {len(chunks)} chunks saved")

if __name__ == "__main__":
    ingest()