# from fastapi import APIRouter, HTTPException, status
# from pydantic import BaseModel
# from executor.registry import get_runner
# from job.models import CodeRunRequest, CodeRunResponse

# router = APIRouter()

# @router.post("/execute", response_model=CodeRunResponse)
# async def execute_code(request: CodeRunRequest):
#     runner = get_runner(request.language, request.version)
#     if not runner:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Unsupported language or version: {request.language}:{request.version}"
#         )
#     result = await runner.run(request.code, request.stdin)
#     return CodeRunResponse(**result)



# import os
# import subprocess

# from fastapi import APIRouter, HTTPException, status
# from pydantic import BaseModel

# from executor.registry import get_runner
# from job.models import CodeRunRequest, CodeRunResponse

# router = APIRouter()

# #
# # 1) MCP‐compatible endpoint on /mcp/run
# #
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

# @router.post("/execute", response_model=RunOutput)
# async def run_code_mcp(input: RunInput) -> RunOutput:
#     """
#     This handler writes the code to /tmp, invokes spark-submit,
#     and returns its stdout/stderr/exit_code.
#     """
#     try:
#         # write into tmpfs
#         base = input.filename or "script.py"
#         if not base.endswith(".py"):
#             base += ".py"
#         tmp_path = os.path.join("/tmp", base)

#         with open(tmp_path, "w") as f:
#             f.write(input.code)

#         # execute
#         result = subprocess.run(
#             ["spark-submit", tmp_path],
#             input=input.stdin.encode() if input.stdin else None,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             timeout=60
#         )

#         os.remove(tmp_path)
#         return RunOutput(
#             stdout=result.stdout.decode(),
#             stderr=result.stderr.decode(),
#             exit_code=result.returncode
#         )
#     except Exception as e:
#         return RunOutput(stdout="", stderr=str(e), exit_code=1)


# #
# # 2) Your custom /execute endpoint
# #
# @router.post("/execute", response_model=CodeRunResponse)
# async def execute_code(request: CodeRunRequest):
#     """
#     Dispatches to the appropriate runner (Python or PySpark).
#     Uses the get_runner registry to call runner.run().
#     """
#     try:
#         runner = get_runner(request.language, request.version)
#     except ValueError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Unsupported language or version: {request.language}:{request.version}"
#         )

#     result = await runner.run(request.code, request.stdin)
#     return CodeRunResponse(**result)




from fastapi import APIRouter, HTTPException, status
from executor.registry import get_runner
from job.models import CodeRunRequest, CodeRunResponse

router = APIRouter()

@router.post("/execute", response_model=CodeRunResponse)
async def execute_code(request: CodeRunRequest):
    try:
        runner = get_runner(request.language, request.version)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    result = await runner.run(request.code, request.stdin or "")
    return CodeRunResponse(**result)

# Optional alias so tools using MCP-ish paths can still work
@router.post("/mcp/execute", response_model=CodeRunResponse)
async def execute_code_mcp(request: CodeRunRequest):
    return await execute_code(request)
