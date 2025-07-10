from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class Category(str, Enum):
    GENERAL = "GENERAL"
    FILE = "FILE"
    FUNCTION_CLASS = "FUNCTION&CLASS"
    FOLLOW_UP = "FOLLOWUP"

class ClassificationOutput(BaseModel):
    label: Category = Field(
        ...,
        description="""
            Label for the user question:
            - GENERAL → question is about the overall repository, its purpose, usage, how to build/run, etc. It does NOT mention any specific file, class, or function name.
            - FILE → question explicitly mentions a SINGLE file name (e.g. utils.py, index.js, Dockerfile, pom.xml, etc.).
            - FUNCTION&CLASS → question explicitly mentions a function or class name (e.g. get_config(), UserController, fetchData, etc.).
            - FOLLOWUP -> the user query is about a previous message or a follow up question, hence requires no context. 
        """
    )


class MultipleFilesSelection(BaseModel):
    file_indices: List[int] = Field(
        description="List of file indices (1-based) relevant to answering the user's question. Return [-1] if no files are relevant."
    )


class SingleFileSelection(BaseModel):
    file_index: int = Field(
        description='The 1-based index of the single matched file from the file list. Return -1 if no matching file is found.'
    )