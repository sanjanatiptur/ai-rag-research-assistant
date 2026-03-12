import requests
import numpy as np

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"

class VectorStore:
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
        self.documents = []
        self.embeddings = []

    def _get_embedding(self, text):
        response = requests.post(
            OLLAMA_EMBED_URL,
            json={
                "model": self.model_name,
                "prompt": text
            }
        )
        return np.array(response.json()["embedding"])

    def add_documents(self, docs):
        for doc in docs:
            embedding = self._get_embedding(doc)
            self.documents.append(doc)
            self.embeddings.append(embedding)

    def similarity_search(self, query, k=2):
        query_embedding = self._get_embedding(query)

        similarities = [
            np.dot(query_embedding, doc_embedding) /
            (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
            for doc_embedding in self.embeddings
        ]

        top_k_indices = np.argsort(similarities)[-k:][::-1]

        return [self.documents[i] for i in top_k_indices]