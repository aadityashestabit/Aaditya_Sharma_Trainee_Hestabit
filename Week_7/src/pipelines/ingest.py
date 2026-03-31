from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, CSVLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import numpy as np
import json
import os
from src.embeddings.embedder import embed

RAW_DATA_DIR = "src/data/raw"
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
            except:
                print(f"Failed: {filepath.name}")
    except:
        pass

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
    except:
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
    except:
        return {}

def ingest():
    try:
        docs   = load_documents()
        chunks = chunk_documents(docs)
    except:
        return

    try:
        texts     = [c.page_content for c in chunks]
        metadatas = [build_metadata(c, i) for i, c in enumerate(chunks)]
    except:
        texts, metadatas = [], []

    try:
        embeddings = embed(texts)
        vectors    = np.array(embeddings, dtype=np.float32)
    except:
        return

    try:
        index = faiss.IndexFlatL2(vectors.shape[1])
        os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    except:
        return

    try:
        BATCH_SIZE = 5000
        for i in range(0, len(vectors), BATCH_SIZE):
            index.add(vectors[i:i+BATCH_SIZE])
            print(f"Stored batch {i//BATCH_SIZE + 1}")
    except:
        pass

    try:
        faiss.write_index(index, f"{VECTORSTORE_DIR}/index.faiss")
    except:
        pass

    try:
        with open(f"{VECTORSTORE_DIR}/store.json", "w") as f:
            json.dump({"texts": texts, "metadatas": metadatas}, f)
    except:
        pass

    print(f"Done — {len(chunks)} chunks saved")

if __name__ == "__main__":
    try:
        ingest()
    except:
        pass