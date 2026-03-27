from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedder loaded: all-MiniLM-L6-v2")

def embed(texts):
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()

def embed_single(text):
    return model.encode([text])[0].tolist()