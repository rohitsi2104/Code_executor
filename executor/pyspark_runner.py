# import asyncio
# import tempfile
# import os
# from executor.base import CodeRunner

# class PySparkRunner(CodeRunner):
#     image = "piston_executor_pyspark:latest"
#     version = "3.1"  # Example version

#     async def run(self, code: str, stdin: str = None):
#         with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as code_file:
#             code_file.write(code.encode())
#             code_path = code_file.name

#         # Use asyncio with subprocess for async execution
#         process = await asyncio.create_subprocess_exec(
#             "spark-submit", code_path,
#             stdin=asyncio.subprocess.PIPE if stdin else None,
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE
#         )
#         stdout, stderr = await process.communicate(input=stdin.encode() if stdin else None)
#         os.remove(code_path)
#         return {
#             "stdout": stdout.decode(),
#             "stderr": stderr.decode(),
#             "exit_code": process.returncode
#         }



import httpx
from executor.base import CodeRunner

class PySparkRunner(CodeRunner):
    image = "piston_executor_pyspark:latest"
    version = "3.1"

    async def run(self, code: str, stdin: str = "") -> dict:
        filename = "script.py"  # Dynamically derived
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://pyspark_runner:8080/mcp/run",
                    json={
                        "language": "pyspark",
                        "version": self.version,
                        "filename": filename,
                        "code": code,
                        "stdin": stdin,
                    }
                )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "exit_code": 1
            }
