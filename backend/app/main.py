from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from git import Repo, GitCommandError
from .schema.user_request import UserStartRequest, UserChatRequest
import os
import shutil
from langchain_core.messages import HumanMessage, SystemMessage
from .utils.ingest_repo import ingest_repo
import stat
from .utils.chat import SYSTEM_PROMPT,LLM_OUTPUT

CHAT_HISTORY=[]
FILE_SYMBOL_TABLE=[]
app = FastAPI(
    title="Codebase Chatbot API",
    description="Ask questions about code repos using RAG & Advanced LLM Reasoning.",
    version="1"
)

def on_rm_error(func, path, exc_info):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
    func(path)

def cleanup():
    workspace_dir = os.path.abspath("workspace")
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir, onerror=on_rm_error)
    
    chroma_code_path = os.path.abspath("/chroma_code_db")
    chroma_noncode_path = os.path.abspath("/chroma_noncode_db")
    for path in [chroma_code_path, chroma_noncode_path]:
        if os.path.exists(path):
            shutil.rmtree(path, onerror=on_rm_error)



@app.get("/")
def home():
    return JSONResponse(status_code=200,content="API For Chatting With Any Public Github Repo!")


@app.post("/init-chat")
def init(request : UserStartRequest):
    CHAT_HISTORY.clear()
    global FILE_SYMBOL_TABLE
    FILE_SYMBOL_TABLE.clear()
    CHAT_HISTORY.append(SystemMessage(content=SYSTEM_PROMPT))

    repo_url = request.repo_url
    repo_name = str(repo_url).rstrip("/").split("/")[-1]

    cleanup()

    workspace_dir = os.path.abspath("workspace")
    new_repo_path = os.path.join(workspace_dir, repo_name)

    try:
        Repo.clone_from(repo_url, new_repo_path, depth=1)
        FILE_SYMBOL_TABLE=ingest_repo(new_repo_path)
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
    
    

@app.post("/start-chat")
def start(request : UserChatRequest):
    query = request.query
    try:
        result = LLM_OUTPUT(query,CHAT_HISTORY,FILE_SYMBOL_TABLE)
        print(result)
        return {
            "message": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
   
    



