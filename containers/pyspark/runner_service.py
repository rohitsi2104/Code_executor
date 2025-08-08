
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio, tempfile, os

app = FastAPI(title="PySpark Runner")


@app.get("/health")
def health():
    return {"ok": True}


class CodeRunRequest(BaseModel):
    language: str
    version: str
    code: str
    stdin: str = ""

class CodeRunResponse(BaseModel):
    stdout: str
    stderr: str
    exit_code: int

@app.post("/execute", response_model=CodeRunResponse)
async def execute(req: CodeRunRequest):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(req.code)
        path = f.name
    try:
        cmd = ["spark-submit", "--master", "local[*]", path]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate((req.stdin or "").encode())
        return CodeRunResponse(
            stdout=out.decode(errors="ignore"),
            stderr=err.decode(errors="ignore"),
            exit_code=proc.returncode
        )
    finally:
        try: os.remove(path)
        except OSError: pass
