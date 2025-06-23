from fastapi import FastAPI
from app.routes import endpoints

app = FastAPI(
    title="Codebase Chatbot API",
    description="Ask questions about code repos using RAG",
    version="0.1.0"
)

app.include_router(endpoints.router)
