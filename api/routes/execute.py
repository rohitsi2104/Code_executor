from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from executor.registry import get_runner
from job.models import CodeRunRequest, CodeRunResponse

router = APIRouter()

@router.post("/execute", response_model=CodeRunResponse)
async def execute_code(request: CodeRunRequest):
    runner = get_runner(request.language, request.version)
    if not runner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported language or version: {request.language}:{request.version}"
        )
    result = await runner.run(request.code, request.stdin)
    return CodeRunResponse(**result)
