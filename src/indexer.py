import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

class AuraIndexer:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.rows = None

    def build_index(self, rows):
        self.rows = rows

        embeddings = []
        for r in tqdm(rows, desc="Embedding steps"):
            emb = self.model.encode(r["text"], normalize_embeddings=True)
            embeddings.append(emb)

        embeddings = np.array(embeddings).astype("float32")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # cosine similarity
        self.index.add(embeddings)

    def search(self, query, top_k=6):
        q_emb = self.model.encode(query, normalize_embeddings=True).astype("float32")
        q_emb = np.expand_dims(q_emb, axis=0)

        scores, idx = self.index.search(q_emb, top_k)

        results = []
        for j, i in enumerate(idx[0]):
            if i == -1:
                continue
            results.append({
                "score": float(scores[0][j]),
                **self.rows[i]
            })
        return results
