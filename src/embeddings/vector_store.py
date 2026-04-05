import faiss
import numpy as np


class VectorStore:
    """
    FAISS-based vector store for storing and searching text chunk embeddings.
    Dimension is inferred automatically from the first batch of embeddings.
    """

    def __init__(self, dimension=None):
        self.index = None
        self.text_chunks = []
        self.dimension = dimension

        # If dimension provided upfront, build index immediately
        if dimension is not None:
            self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings: np.ndarray, texts: list):
        """Add embeddings and their corresponding text chunks to the store."""
        embeddings = np.array(embeddings).astype("float32")

        if self.index is None:
            self.dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(self.dimension)

        self.index.add(embeddings)
        self.text_chunks.extend(texts)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list:
        """Search for the top_k most similar chunks to the query embedding."""
        if self.index is None or len(self.text_chunks) == 0:
            return []

        query_embedding = np.array(query_embedding).astype("float32")

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        top_k = min(top_k, len(self.text_chunks))
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.text_chunks[idx])

        return results