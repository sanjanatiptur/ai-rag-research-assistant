import requests
import numpy as np

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"

documents = [
    "RAG stands for Retrieval-Augmented Generation in AI systems.",
    "FastAPI is a modern Python web framework for building APIs.",
    "Embeddings convert text into numerical vectors for semantic comparison."
]

def get_embedding(text):
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return np.array(response.json()["embedding"])

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Generate embeddings for documents
doc_embeddings = [get_embedding(doc) for doc in documents]

# User query
query = "What is RAG in machine learning?"

query_embedding = get_embedding(query)

# Compute similarities
similarities = [
    cosine_similarity(query_embedding, doc_embedding)
    for doc_embedding in doc_embeddings
]

# Find best match
best_match_index = np.argmax(similarities)

print("Query:", query)
print("Best matched document:")
print(documents[best_match_index])