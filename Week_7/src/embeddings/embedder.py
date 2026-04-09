from sentence_transformers import SentenceTransformer

try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    vec = model.encode(["test sentence"])
    print(f"Vector dimension: {vec.shape[1]}")
    print(f"Max token limit: {model.max_seq_length}")
    print("Embedder loaded: all-MiniLM-L6-v2")
except:
    model = None

def embed(texts):
    try:
        embeddings = model.encode(texts, show_progress_bar=True) if model is not None else []
        return embeddings.tolist()
    except:
        return []

def embed_single(text):
    try:
        return model.encode([text])[0].tolist() if model is not None else []
    except:
        return []