from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    TextLoader,
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredRSTLoader,
    NotebookLoader
)
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
#CODE_EMBEDDING_MODEL = VoyageEmbeddings(model="voyage-code-3")
CODE_EMBEDDING_MODEL = OpenAIEmbeddings(model="provider-3/text-embedding-3-small")
NON_CODE_EMBEDDING_MODEL = OpenAIEmbeddings(model="provider-3/text-embedding-3-small")
EXT_TO_LANGUAGE = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".ts": Language.TS,
    ".java": Language.JAVA,
    ".cpp": Language.CPP,
    ".c": Language.C,
    ".go": Language.GO,
    ".rs": Language.RUST,
    ".rb": Language.RUBY,
    ".php": Language.PHP,
    ".cs": Language.CSHARP,
    ".swift": Language.SWIFT,
    ".kt": Language.KOTLIN,
    ".scala": Language.SCALA,
    ".html": Language.HTML,
    ".htm":Language.HTML
}

EXT_TO_LOADER = {
    ".md": UnstructuredMarkdownLoader,
    ".txt": TextLoader,
    ".log":TextLoader,
    ".gitignore": TextLoader,
    ".rst": UnstructuredRSTLoader,
    ".pdf": UnstructuredPDFLoader,
    ".docx": UnstructuredWordDocumentLoader,
    ".ipynb": NotebookLoader,
    ".yml": TextLoader,
    ".yaml": TextLoader,
    ".json": TextLoader,
    ".toml": TextLoader,
    ".xml": TextLoader,  
    ".tex": TextLoader,
}


def code_file_chunks(lang_enum,file_path):
    splitter = RecursiveCharacterTextSplitter.from_language(language=lang_enum)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()
        chunks = splitter.split_text(code)

    return chunks


def non_code_file_chunks(DATA):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(DATA)

    return chunks



def save_code_embeddings(code_files_info):
    ALL_CHUNKS = []
    METADATA = []

    for f in code_files_info:
        for i, chunk in enumerate(f["chunks"]):
            ALL_CHUNKS.append(chunk)
            METADATA.append({
                "file_path": f["path"],
                "language": f["language"],
                "chunk_id": i
            })

    CODE_VECTOR_STORE = Chroma.from_texts(
                    collection_name="repo_code_chunks",
                    texts=ALL_CHUNKS,
                    embedding=CODE_EMBEDDING_MODEL,
                    metadatas=METADATA,
                    persist_directory="../chroma_code_db"
                )



def save_non_code_embeddings(non_code_files_info):
    ALL_CHUNKS = []
    METADATA = []

    for f in non_code_files_info:
        for i, chunk in enumerate(f["chunks"]):
            ALL_CHUNKS.append(chunk.page_content)
            METADATA.append({
                "file_path": f["path"],
                "language":f["language"],
                "chunk_id": i
            })
    
    NONCODE_VECTOR_STORE = Chroma.from_texts(
        collection_name="repo_noncode_chunks",
        texts=ALL_CHUNKS,
        embedding=CODE_EMBEDDING_MODEL,
        metadatas=METADATA,
        persist_directory="../chroma_noncode_db"
    )


def ingest_repo(repo_path):
    CODE_FILES_INFO = []
    FILES_SYMBOL_TABLE = []
    NON_CODE_FILES_INFO = []
    repo_path = Path(repo_path)

    for filepath in repo_path.rglob("*"):
        if filepath.is_file():
            filename = filepath.name
            ext = filepath.suffix.lower()
            FILES_SYMBOL_TABLE.append(
                {
                    "path":str(filepath),
                    "language":ext,
                    "filename": filename
                }
            )

            if ext in EXT_TO_LANGUAGE:
                lang_enum = EXT_TO_LANGUAGE[ext]
                chunks = code_file_chunks(lang_enum,filepath)
                CODE_FILES_INFO.append({
                    "path": str(filepath),
                    "language": lang_enum.name,
                    "chunks": chunks
                })

            if ext in EXT_TO_LOADER:
                loader_cls = EXT_TO_LOADER[ext]
                loader = loader_cls(filepath,encoding="utf-8")
                docs = loader.load()
                chunks = non_code_file_chunks(docs)
                NON_CODE_FILES_INFO.append({
                    "path": str(filepath),
                    "language":ext,
                    "chunks": chunks
                })
            
    #print(CODE_FILES_INFO)

    save_code_embeddings(CODE_FILES_INFO)
    save_non_code_embeddings(NON_CODE_FILES_INFO)

