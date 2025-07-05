from pydantic import BaseModel, HttpUrl, Field, field_validator

class UserStartRequest(BaseModel):
    repo_url: HttpUrl = Field(
        ...,
        description="Public HTTPS URL of the GitHub repository to be cloned.",
        example="https://github.com/fastapi/fastapi"
    )


    @field_validator("repo_url")
    @classmethod
    def validate_github_url(cls, v: HttpUrl):
        if not v.host or v.host != "github.com":
            raise ValueError("Only 'github.com' URLs are allowed")
        if not v.scheme.startswith("http"):
            raise ValueError("Only HTTPS URLs are allowed")
        if len(v.path.strip("/").split("/")) < 2:
            raise ValueError("Invalid GitHub repo URL format. Must be like 'https://github.com/user/repo'")
        return v
    


class UserChatRequest(BaseModel):
    query : str = Field(
        ...,
        description="Your Question about the repo",
        example="What is this repo about ?"
    )