# CodeWhisper 🧠💬

**CodeWhisper** is a conversational AI tool that allows you to interact with GitHub repositories using natural language. It's designed to help you explore and understand large codebases faster by providing a clean, modern chat interface to ask questions about the code.

---
## ⚠️ Important Note

Due to free-tier hosting and limited server resources, **only repositories under ~30 MB in size** are currently supported.  

---

## ✨ Overview

Have you ever felt lost in a new or complex GitHub repository? CodeWhisper is here to help. Instead of spending hours manually searching through files and folders, you can simply ask questions in plain English. CodeWhisper leverages the power of Large Language Models (LLMs) to understand your queries and provide context-aware answers, making codebase exploration more intuitive and efficient.

Why CodeWhisper is useful:
- **Explore large codebases faster:** Get to the information you need without getting lost in the file tree.
- **Understand complex logic:** Ask for explanations of specific functions, classes, or files.
- **Onboard new developers quickly:** Help new team members get up to speed with a new codebase.

---

## 🧰 Tech Stack

CodeWhisper is built with a modern, powerful tech stack:

-   **Frontend:** React.js
-   **Backend:** FastAPI server using LangChain for LLM-related tasks
-   **LLM:** GPT-4.1 nano
-   **RAG System:** Dynamic Retrieval-Augmented Generation

---

## 🔍 Key Features

-   **🧠 Intelligent Query Understanding:** CodeWhisper understands natural language queries and can interpret your intent to find the most relevant information.
-   **📂 Context-Aware Response Generation:** The dynamic RAG system provides context from the repository to the LLM, resulting in more accurate and relevant answers.
-   **⚡ Fast Repo Exploration:** Quickly navigate and understand repositories of any size.
-   **💬 Clean, Modern Chat UI:** A user-friendly interface that makes interacting with your codebase a breeze.

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

## 🚀 How to Run Locally
### 📦 1. Clone the Repo

```bash
git clone https://github.com/your-username/code-whisper.git
cd code-whisper
```

---

### 🖥️ 2. Backend Setup

```bash
cd backend
python3.10 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in root (`code-whisper/.env`) with:
```env
OPENAI_API_KEY=your_api_key_here
```

Run the FastAPI server:
```bash
uvicorn app.main:app --reload
```

> Runs at: `http://127.0.0.1:8000`

---

### 🌐 3. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

> Runs at: `http://localhost:3000`

---

## ⚙️ Architecture

CodeWhisper's architecture is designed for modularity and scalability. Here's a brief overview of the components:

-   **Frontend:** A React.js application that provides the user interface for the chat.
-   **Backend:** A FastAPI server that handles the core logic. It receives user queries, interacts with the LLM via LangChain, and manages the RAG system.
-   **LLM (Large Language Model):** We use GPT-4.1 nano for its powerful natural language understanding and generation capabilities.
-   **Vector Store:** A vector database (like ChromaDB) is used to store embeddings of the codebase for efficient retrieval.
-   **Dynamic RAG System:** This system dynamically retrieves relevant context from the vector store based on the user's query and injects it into the prompt for the LLM.

---

## 📸 Screenshots

*(Placeholder for a GIF or screenshot of the CodeWhisper chat interface)*

---

## 📦 Dependencies

-   **LangChain:** For building the core LLM-powered application.
-   **ChromaDB (or other vector DB):** For creating and managing the vector store.
-   **OpenAI API (or similar):** For accessing the LLM.
-   **React.js:** For the frontend user interface.
-   **FastAPI:** For the backend server.
-   **GitPython:** For cloning and managing GitHub repositories.

---

## 🤖 Example Queries

Here are a few examples of questions you can ask CodeWhisper:

-   "What does `train.py` do?"
-   "Show me all functions that use the `load_model()` function."
-   "Where is the database configuration defined?"
-   "Explain the `CustomDataset` class in `data_loader.py`."

---

## 🌐 Deployed Project

You can find the live version of CodeWhisper here:
[**Link to Deployed Project**](https://your-deployment-link.com) (coming soon!)

---

## ✍️ Author
**Nikhil Kumar**
