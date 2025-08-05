import asyncio
import tempfile
import os
from executor.base import CodeRunner

class PythonRunner(CodeRunner):
    def __init__(self, version: str):
        super().__init__()
        self.version = version

    async def run(self, code: str, stdin: str):
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as src:
            src.write(code.encode())
            src_path = src.name

        try:
            proc = await asyncio.create_subprocess_exec(
                f"python{self.version}", src_path,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate(stdin.encode())
            return {
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "exit_code": proc.returncode
            }
        finally:
            try:
                os.remove(src_path)
            except OSError:
                pass
