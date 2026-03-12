import requests
from vector_store import VectorStore

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()

    def ingest_documents(self, documents):
        self.vector_store.add_documents(documents)

    def generate_answer(self, query, k=2):
        # Step 1: Retrieve relevant documents
        retrieved_docs = self.vector_store.similarity_search(query, k=k)

        # Step 2: Build context
        context = "\n".join(retrieved_docs)

        # Step 3: Build grounded prompt
        prompt = f"""
You are an AI assistant.

Use ONLY the context below to answer the question.

Context:
{context}

Question:
{query}

Answer:
"""

        # Step 4: Call LLM
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

        return {
            "answer": result.get("response", ""),
            "retrieved_context": retrieved_docs
        }