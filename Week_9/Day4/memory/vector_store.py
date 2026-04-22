import os
import pickle
import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("[Warning] faiss-cpu not installed.")

try:
    from sentence_transformers import SentenceTransformer
    ST_AVAILABLE = True
except ImportError:
    ST_AVAILABLE = False
    print("[Warning] sentence-transformers not installed.")


class FaissVectorStore:
    def __init__(
        self,
        index_path: str = "memory/vector.index",
        metadata_path: str = "memory/vector_metadata.pkl",
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.metadata = []   # stores text + extra info alongside each vector
        self.index = None
        self.encoder = None

        if not FAISS_AVAILABLE or not ST_AVAILABLE:
            print("[VectorStore] Running in disabled mode — install faiss-cpu and sentence-transformers.")
            return

        self.encoder = SentenceTransformer(model_name)
        dim = self.encoder.get_sentence_embedding_dimension()

        # load existing index from disk if available, otherwise start fresh
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            self.index = faiss.read_index(index_path)
            with open(metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
            print(f"[VectorStore] Loaded existing index — {self.index.ntotal} vectors")
        else:
            self.index = faiss.IndexFlatL2(dim)
            print(f"[VectorStore] New index created (dim={dim})")

    def _encode(self, text: str) -> np.ndarray:
        vec = self.encoder.encode([text], convert_to_numpy=True)
        return vec.astype("float32")

    def add_text(self, text: str, metadata: dict = None):
        if not self._is_ready():
            return
        vec = self._encode(text)
        self.index.add(vec)
        self.metadata.append({"text": text, **(metadata or {})})
        self._save()

    def search(self, query: str, k: int = 3) -> list:
        if not self._is_ready() or self.index.ntotal == 0:
            return []
        vec = self._encode(query)
        k = min(k, self.index.ntotal)  # can't ask for more than what exists
        distances, indices = self.index.search(vec, k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                results.append({
                    "text": self.metadata[idx]["text"],
                    "score": float(dist),
                    "meta": self.metadata[idx],
                })
        return results

    def format_search_results(self, results: list) -> str:
        if not results:
            return "No similar context found."
        lines = []
        for i, r in enumerate(results, 1):
            role = r["meta"].get("role", "unknown")
            lines.append(f"{i}. [{role}] {r['text'][:200]}")
        return "\n".join(lines)

    def _save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True) if os.path.dirname(self.index_path) else None
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def _is_ready(self) -> bool:
        return FAISS_AVAILABLE and ST_AVAILABLE and self.index is not None and self.encoder is not None

    @property
    def total_vectors(self) -> int:
        return self.index.ntotal if self._is_ready() else 0