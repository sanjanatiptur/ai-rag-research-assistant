import requests
import numpy as np

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"

# Sample documents (acting as chunks)
documents = [
    "RAG stands for Retrieval-Augmented Generation in AI systems.",
    "FastAPI is a modern Python web framework for building APIs.",
    "Embeddings convert text into numerical vectors for semantic comparison.",
    "RAG improves factual accuracy by grounding responses in retrieved documents."
]

# ---- EMBEDDING FUNCTION ----
def get_embedding(text):
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return np.array(response.json()["embedding"])

# ---- COSINE SIMILARITY ----
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# ---- GENERATE EMBEDDINGS FOR DOCUMENTS ----
doc_embeddings = [get_embedding(doc) for doc in documents]

# ---- USER QUERY ----
query = "Explain what RAG is and why it improves accuracy."

query_embedding = get_embedding(query)

# ---- COMPUTE SIMILARITIES ----
similarities = [
    cosine_similarity(query_embedding, doc_embedding)
    for doc_embedding in doc_embeddings
]

# ---- RETRIEVE TOP-K DOCUMENTS ----
k = 2
top_k_indices = np.argsort(similarities)[-k:][::-1]

retrieved_docs = [documents[i] for i in top_k_indices]

# ---- BUILD CONTEXT ----
context = "\n".join(retrieved_docs)

# ---- BUILD PROMPT ----
prompt = f"""
You are an AI assistant.

Use ONLY the context below to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

# ---- SEND TO LLM ----
response = requests.post(
    OLLAMA_GENERATE_URL,
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    },
    timeout=180
)

result = response.json()

print("\nRetrieved Context:\n")
print(context)

print("\nGenerated Answer:\n")
print(result["response"])