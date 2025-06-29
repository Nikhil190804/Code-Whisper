from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from git import Repo, GitCommandError
from .schema.user_request import UserRequest
import os

app = FastAPI(
    title="Codebase Chatbot API",
    description="Ask questions about code repos using RAG.",
    version="1"
)

@app.get("/")
def home():
    return JSONResponse(status_code=200,content="API For Chatting With Any Public Github Repo!")


@app.post("/start-chat")
def start(request : UserRequest):
    repo_url = request.repo_url
    repo_name = str(repo_url).rstrip("/").split("/")[-1]

    workspace_dir = os.path.abspath("workspace")
    new_repo_path = os.path.join(workspace_dir, repo_name)

    try:
        Repo.clone_from(repo_url, new_repo_path, depth=1)
        return {
            "message": "Repository cloned successfully",
            "local_path": new_repo_path
        }
    except GitCommandError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Repository not found or private")
        elif "authentication" in str(e).lower():
            raise HTTPException(status_code=401, detail="Authentication failed")
        else:
            raise HTTPException(status_code=400, detail=f"Git error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    
    



