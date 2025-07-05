from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class Category(str, Enum):
    GENERAL = "GENERAL"
    FILE = "FILE"
    FUNCTION_CLASS = "FUNCTION&CLASS"

class ClassificationOutput(BaseModel):
    label: Category = Field(
        ...,
        description="""
            Label for the user question:
            - GENERAL → question is about the overall repository, its purpose, usage, how to build/run, etc. It does NOT mention any specific file, class, or function name.
            - FILE → question explicitly mentions a SINGLE file name (e.g. utils.py, index.js, Dockerfile, pom.xml, etc.).
            - FUNCTION&CLASS → question explicitly mentions a function or class name (e.g. get_config(), UserController, fetchData, etc.).
        """
    )


class MultipleFilesSelection(BaseModel):
    files: List[str] = Field(
        description="List of full file paths relevant to answering the user's question."
    )



class SingleFileSelection(BaseModel):
    file_path: str = Field(
        description='Full path to the matched file in the repository. Return "-1" if no matching file is found.'
    )