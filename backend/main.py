from fastapi import FastAPI
from pydantic import BaseModel
from services.rag_service import RAGService
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


# Create ONE global instance
rag_service = RAGService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    demo_documents = [
        "RAG stands for Retrieval-Augmented Generation in AI systems.",
        "RAG improves factual accuracy by grounding responses in retrieved documents.",
        "FastAPI is a modern Python web framework for building APIs."
    ]
    rag_service.ingest_documents(demo_documents)

    yield

    # Shutdown logic (if needed later)
    print("Shutting down application...")

app = FastAPI(    title="AI News Research Backend (RAG)",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestRequest(BaseModel):
    documents: list[str]

class AskRequest(BaseModel):
    question: str

@app.post("/ingest")
def ingest_documents(request: IngestRequest):
    rag_service.ingest_documents(request.documents)
    return {"status": "Documents ingested successfully"}

@app.post("/ask")
def ask_question(request: AskRequest):
    result = rag_service.generate_answer(request.question)
    return result