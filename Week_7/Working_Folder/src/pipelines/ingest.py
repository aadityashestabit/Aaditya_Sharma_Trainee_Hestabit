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

# loading documents \
def load_documents():
    docs = []
    supported = {".pdf", ".docx", ".csv", ".txt"}

    try:
        # rglob finds supported files recursively 
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

# document chunking 
# -- 800 character chunk , --150 character overlap 
def chunk_documents(docs):
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " "] # seperate on natural boundaries
        )
        chunks = splitter.split_documents(docs)
        print(f"Created {len(chunks)} chunks")
        return chunks
    except Exception as e:
        print(f"Error chunking documents: {type(e).__name__}: {e}")
        return []
    
# takes metadata langchain already attached and adds more fields  
def build_metadata(chunk, idx):
    try:
        meta = chunk.metadata.copy()
        meta["chunk_id"] = f"chunk_{idx}" # used by hybrid retriever to merge bm25 resukts 
        meta["source"]   = meta.get("source", "unknown")
        meta["page"]     = meta.get("page", 0)  # used in deduplication
        meta["tags"]     = "enterprise_doc"  # fixed tags for all chunks 

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
        docs   = load_documents() # loading
        chunks = chunk_documents(docs) # chunking 
    except Exception as e:
        print(f"Error during document loading/chunking: {type(e).__name__}: {e}")
        return

    if not chunks:
        print("No chunks to process. Exiting.")
        return

    try:
        texts     = [c.page_content for c in chunks] # extract just text context from chunks and passed to embedder  
        metadatas = [build_metadata(c, i) for i, c in enumerate(chunks)] # extracts metadata
    except Exception as e:
        print(f"Error extracting texts/metadatas: {type(e).__name__}: {e}")
        texts, metadatas = [], []

    try:
        embeddings = embed(texts) # embedding 
        vectors    = np.array(embeddings, dtype=np.float32)
    except Exception as e:
        print(f"Error generating embeddings: {type(e).__name__}: {e}")
        return

    try:
        os.makedirs(VECTORSTORE_DIR, exist_ok=True)
        dim   = vectors.shape[1] # 768 
        index = faiss.IndexFlatL2(dim) #exact search — checks every single vector, no approximation
        index.add(vectors) # loads all vector in memory 
        print(f"FAISS index created — {index.ntotal} vectors, dim={dim}")
    except Exception as e:
        print(f"Error creating FAISS index: {type(e).__name__}: {e}")
        return
    
    
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