from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from git import Repo, GitCommandError
from .schema.user_request import UserRequest

app = FastAPI(
    title="Codebase Chatbot API",
    description="Ask questions about code repos using RAG.",
    version="1"
)

@app.get("/")
def home():
    return JSONResponse(status_code=200,content="API For Chatting With Any Public Github Repo!")



