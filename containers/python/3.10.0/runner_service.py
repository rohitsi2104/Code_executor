from fastapi import FastAPI
from pydantic import BaseModel
import asyncio, tempfile, os, sys

app = FastAPI(title="Python Runner")

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
        proc = await asyncio.create_subprocess_exec(
            sys.executable, path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate((req.stdin or "").encode())
        return CodeRunResponse(stdout=out.decode(), stderr=err.decode(), exit_code=proc.returncode)
    finally:
        try: os.remove(path)
        except OSError: pass
