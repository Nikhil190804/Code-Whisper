# 🧠 Repo Chat — Codebase Q&A Server (FastAPI + LangChain)

**Repo Chat** is a backend server built with **FastAPI**, designed to let users interact with any **public GitHub repository** using natural language queries. It uses a combination of **LangChain**, symbol tables, and smart query filtering to answer questions about the structure, logic, and usage of codebases.

---


## ⚠️ Important Note

Due to free-tier hosting and limited server resources, **only repositories under ~30 MB in size** are currently supported.  

---
## 🚀 Features

- Clone and analyze any public GitHub repository.
- Ask natural-language questions about code structure, functions, files, or setup.
- Uses RAG (Retrieval-Augmented Generation) selectively, only when relevant.
- Intelligent **query categorization** and **dynamic context feeding**.
- In-memory chat history and symbol table for each session.
- API-first design using **FastAPI**, easily integratable with a frontend (e.g. React).
- Deployed and tested on **Render.com**.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** – REST API framework
- **LangChain** – for LLM reasoning and document retrieval
- **GitPython** – clone and manage GitHub repos
- **Pydantic** – request validation
- **shutil / os / stat** – workspace and file management
- **CORS middleware** – for cross-origin frontend integration

---

## 📦 API Endpoints

### `GET /`

Returns a welcome message confirming the API is live.

**Response:**

```json
"API For Chatting With Any Public Github Repo!"
```

---

### `POST /init-chat`

Clones the repo and initializes the chat session.

**Request Payload:**

```json
{
  "repo_url": "https://github.com/owner/repo"
}
```

**Success Response:**

```json
{
  "message": "Repository cloned successfully",
  "local_path": "/absolute/path/to/local/clone"
}
```

**Possible Errors:**

- `404` – Repository not found or private
- `401` – Authentication failed
- `400` – Other Git errors

---

### `POST /start-chat`

Ask questions about the initialized repo.

**Request Payload:**

```json
{
  "query": "Where is the training code in this repo?"
}
```

**Success Response:**

```json
{
  "message": "The training logic is implemented in train.py under the /models directory..."
}
```

---

### `GET /memory`

Returns available disk space and lists current workspace files.

**Success Response:**

```json
{
  "disk": {
    "total_gb": 500,
    "used_gb": 123,
    "free_gb": 377
  },
  "files_in_workspace": [
    "workspace/repo1/file.py",
    "workspace/repo2/utils/helper.py"
  ]
}
```

---

## 🧠 How It Works

- On `/init-chat`, the repo is cloned and parsed.
- A **symbol table** is generated to track file, class, and function metadata.
- User questions are analyzed:
  - If the question targets specific parts (file/class/function), RAG is triggered.
  - Otherwise, relevant code chunks are selected manually and passed as context.
- Responses are generated using a connected LLM.

> 💡 The server supports proxy LLM usage via [a4f.co](https://www.a4f.co/) to avoid high API costs in personal projects.

---

## 🧪 Deployment

This backend is currently deployed on **Render.com**, and is compatible with any frontend (such as a React chat interface).

---

## 📁 Project Structure

```
.
├── main.py                  # FastAPI app with endpoints
├── schema/                  # Pydantic models
├── utils/
│   ├── ingest_repo.py       # Repo parsing + embedding
│   ├── chat.py              # Chat logic + LLM pipeline
├── workspace/               # Temporary repo storage
```

---

## ✍️ Author
**Nikhil Kumar** 
