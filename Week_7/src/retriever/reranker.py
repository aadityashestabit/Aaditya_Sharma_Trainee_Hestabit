from sentence_transformers import CrossEncoder

# load once at module level
try:
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    # this works seperately from normal embeddings this can process query and chunks together
    print("Reranker loaded")
except:
    model = None

def rerank(query, chunks, top_k=5):
    try:
        pairs = [(query, chunk["text"]) for chunk in chunks]
    except:
        return []

    try:
        scores = model.predict(pairs) if model is not None else [] # scoring
    except:
        return []

    try:
        for chunk, score in zip(chunks, scores): # attach scores and sort them 
            chunk["rerank_score"] = round(float(score), 4)

        return sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)[:top_k] # sort on basis of reranked score 
    
    # after this step chunk have 
#     {
#     "semantic_score": 0.57,
#     "bm25_score":     1.0,
#     "hybrid_score":   0.74,
#     "rerank_score":   7.36   ← added here
#   }
    except:
        return []