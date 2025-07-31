from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
import subprocess
import os

# ✅ Manually define these because fastapi-mcp doesn't export them
class RunInput(BaseModel):
    language: str
    version: str
    filename: str
    code: str
    stdin: str = ""

class RunOutput(BaseModel):
    stdout: str
    stderr: str
    exit_code: int

# ✅ Setup FastAPI and MCP
app = FastAPI(title="PySpark MCP Executor")
mcp = FastApiMCP(app)

# ✅ Define normal FastAPI route (no run_handler)
@app.post("/mcp/run")
async def run_code_mcp(input: RunInput) -> RunOutput:
    try:
        filename = input.filename or "script.py"
        if not filename.endswith(".py"):
            filename += ".py"

        with open(filename, "w") as f:
            f.write(input.code)

        result = subprocess.run(
            ["spark-submit", filename],
            input=input.stdin.encode() if input.stdin else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )

        os.remove(filename)

        return RunOutput(
            stdout=result.stdout.decode(),
            stderr=result.stderr.decode(),
            exit_code=result.returncode
        )
    except Exception as e:
        return RunOutput(stdout="", stderr=str(e), exit_code=1)

# ✅ Still mount MCP (for /mcp OpenAPI, etc.)
mcp.mount()
