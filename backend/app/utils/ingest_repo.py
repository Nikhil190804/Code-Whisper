from langchain_community.embeddings import VoyageEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
CODE_EMBEDDING_MODEL = VoyageEmbeddings(model="voyage-code-3")
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
    ".md":Language.MARKDOWN
}


def code_file_chunks(lang_enum,file_path):
    splitter = RecursiveCharacterTextSplitter.from_language(language=lang_enum)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()
        chunks = splitter.split_text(code)

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

    VECTOR_STORE = Chroma.from_texts(
                    collection_name="repo_code_chunks",
                    texts=ALL_CHUNKS,
                    embedding=CODE_EMBEDDING_MODEL,
                    metadatas=METADATA,
                    persist_directory="../chroma_db"
                )
    
    query = "how is the app called here ?"

    results = VECTOR_STORE.similarity_search(query, k=1)

    for res in results:
        print("Content:", res.page_content)
        print("Metadata:", res.metadata)
        print("----------")


def ingest_repo(repo_path):
    CODE_FILES_INFO = []
    FILES_SYMBOL_TABLE = []
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
    #print(CODE_FILES_INFO)

    save_code_embeddings(CODE_FILES_INFO)



ingest_repo("C:\\Users\\DELL\\Desktop\\RepoChat\\backend\\workspace\\RepoChat")