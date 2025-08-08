
# import os
# import subprocess
# from fastapi import FastAPI
# from fastapi_mcp import FastApiMCP
# from pydantic import BaseModel
# from config.settings import init_security

# # ── Apply security hardening before anything else ──
# init_security()

# # ✅ Manually define these because fastapi-mcp doesn't export them
# class RunInput(BaseModel):
#     language: str
#     version: str
#     filename: str
#     code: str
#     stdin: str = ""

# class RunOutput(BaseModel):
#     stdout: str
#     stderr: str
#     exit_code: int

# # ✅ Setup FastAPI and MCP
# app = FastAPI(title="PySpark MCP Executor")
# mcp = FastApiMCP(app)

# # ✅ Define normal FastAPI route (no run_handler)
# @app.post("/mcp/run")
# async def run_code_mcp(input: RunInput) -> RunOutput:
#     try:
#         # Write the user code into a writable tmpfs directory
#         base = input.filename or "script.py"
#         if not base.endswith(".py"):
#             base += ".py"
#         tmp_path = os.path.join("/tmp", base)

#         with open(tmp_path, "w") as f:
#             f.write(input.code)

#         # Execute via spark-submit
#         result = subprocess.run(
#             ["spark-submit", tmp_path],
#             input=input.stdin.encode() if input.stdin else None,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             timeout=60
#         )

#         # Clean up
#         try:
#             os.remove(tmp_path)
#         except OSError:
#             pass

#         return RunOutput(
#             stdout=result.stdout.decode(),
#             stderr=result.stderr.decode(),
#             exit_code=result.returncode
#         )
#     except Exception as e:
#         return RunOutput(stdout="", stderr=str(e), exit_code=1)

# # ✅ Still mount MCP (for /mcp OpenAPI, etc.)
# mcp.mount()







# import os
# from fastapi import FastAPI
# from fastapi_mcp import FastApiMCP

# # bring in your security init
# from config.settings import init_security, API_HOST, API_PORT

# # import your single router (which now handles both /mcp/run and /execute)
# from api.routes.execute import router as execution_router

# # ── Apply all in-process hardening before anything else ──
# init_security()

# # ── FastAPI setup ──
# app = FastAPI(title="PySpark MCP Executor")

# # include your combined execution router
# app.include_router(execution_router)

# # mount MCP on /mcp
# mcp = FastApiMCP(app)
# mcp.mount()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)




# api/main.py
import os
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from config.settings import init_security, API_HOST, API_PORT
from api.routes.execute import router as execution_router

app = FastAPI(title="Code Executor API")   # <-- define app first
app.include_router(execution_router)

mcp = FastApiMCP(app)
mcp.mount()

@app.on_event("startup")
def _secure_startup():
    # Runs AFTER imports; reads env flags (DISABLE_DNS) safely
    init_security()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)
