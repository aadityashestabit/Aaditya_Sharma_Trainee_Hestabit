from sentence_transformers import SentenceTransformer

try:
    model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    
    # model.encode() handles tokenization + embeddings all internally 
    
    # max token input -> 512
    # max db dimension -> 768
    
    
    # verify model working --   
    vec   = model.encode(["test sentence"], normalize_embeddings=True)
    print("Embedder loaded: BAAI/bge-base-en-v1.5")
except Exception as e:
    print(f"Failed to load embedder: {e}")
    model = None

def embed(texts):
    if not texts or model is None:
        print("Warning: empty texts or model not loaded")
        return [] # helps from breaking faiss emoty array pass
    try:
        embeddings = model.encode(
            texts, # lost of chunk strings 
            show_progress_bar=True,
            batch_size=32,
            normalize_embeddings=True  # required for BGE models
        )
        print(f"Generated {len(embeddings)} embeddings, dim={embeddings.shape[1]}")
        return embeddings.tolist()
    except Exception as e:
        print(f"Embedding error: {e}")
        return []

# used during search 

def embed_single(text):
    if not text or not text.strip() or model is None:
        return []
    try:
        embedding = model.encode(
            text,                      # single string — returns shape (768,)
            normalize_embeddings=True
        )
        return embedding.tolist()      # no [0] — already 1D array
    except Exception as e:
        print(f"embed_single error: {e}")
        return []