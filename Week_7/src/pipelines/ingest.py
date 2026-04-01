from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, CSVLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import numpy as np
import json
import os
from src.embeddings.embedder import embed

BASE_DIR      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "src", "data", "raw")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "src", "vectorstore")  

def load_documents():
    docs = []
    supported = {".pdf", ".docx", ".csv", ".txt"}

    try:
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
                print(f"Failed to load '{filepath.name}': {type(e).__name__}: {e}")
    except Exception as e:
        print(f"Error scanning RAW_DATA_DIR '{RAW_DATA_DIR}': {type(e).__name__}: {e}")

    return docs

def chunk_documents(docs):
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " "]
        )
        chunks = splitter.split_documents(docs)
        print(f"Created {len(chunks)} chunks")
        return chunks
    except Exception as e:
        print(f"Error chunking documents: {type(e).__name__}: {e}")
        return []

def build_metadata(chunk, idx):
    try:
        meta = chunk.metadata.copy()
        meta["chunk_id"] = f"chunk_{idx}"
        meta["source"]   = meta.get("source", "unknown")
        meta["page"]     = meta.get("page", 0)
        meta["tags"]     = "enterprise_doc"

        source = meta["source"].lower()
        if source.endswith(".pdf"):    meta["file_type"] = "pdf"
        elif source.endswith(".docx"): meta["file_type"] = "docx"
        elif source.endswith(".csv"):  meta["file_type"] = "csv"
        elif source.endswith(".txt"):  meta["file_type"] = "txt"
        else:                          meta["file_type"] = "unknown"

        return meta
    except Exception as e:
        print(f"Error building metadata for chunk {idx}: {type(e).__name__}: {e}")
        return {}

def ingest():
    try:
        docs   = load_documents()
        chunks = chunk_documents(docs)
    except Exception as e:
        print(f"Error during document loading/chunking: {type(e).__name__}: {e}")
        return

    if not chunks:
        print("No chunks to process. Exiting.")
        return

    try:
        texts     = [c.page_content for c in chunks]
        metadatas = [build_metadata(c, i) for i, c in enumerate(chunks)]
    except Exception as e:
        print(f"Error extracting texts/metadatas: {type(e).__name__}: {e}")
        texts, metadatas = [], []

    try:
        embeddings = embed(texts)
        vectors    = np.array(embeddings, dtype=np.float32)
    except Exception as e:
        print(f"Error generating embeddings: {type(e).__name__}: {e}")
        return

    try:
        index = faiss.IndexFlatL2(vectors.shape[1])
        os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    except Exception as e:
        print(f"Error initializing FAISS index or creating vectorstore dir: {type(e).__name__}: {e}")
        return

# No batching required for <500,000 ch
    try:
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)  # clean and simple
    except Exception as e:
        print(f"Error adding vectors to FAISS index: {type(e).__name__}: {e}")

    try:
        faiss.write_index(index, f"{VECTORSTORE_DIR}/index.faiss")
    except Exception as e:
        print(f"Error saving FAISS index to disk: {type(e).__name__}: {e}")

    try:
        with open(f"{VECTORSTORE_DIR}/store.json", "w") as f:
            json.dump({"texts": texts, "metadatas": metadatas}, f)
    except Exception as e:
        print(f"Error saving store.json: {type(e).__name__}: {e}")

    print(f"Done — {len(chunks)} chunks saved")

if __name__ == "__main__":
    try:
        ingest()
    except Exception as e:
        print(f"Unexpected top-level error: {type(e).__name__}: {e}")