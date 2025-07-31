from typing import Optional
from pydantic import BaseModel

class CodeRunRequest(BaseModel):
    language: str
    version: str
    code: str
    stdin: Optional[str] = ""

class CodeRunResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int
