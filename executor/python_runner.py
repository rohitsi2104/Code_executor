import asyncio
import tempfile
import os
from executor.base import BaseRunner

class PythonRunner(BaseRunner):
    def __init__(self, version: str):
        super().__init__()
        self.version = version  # e.g. "3.10.0" or "3.11.0"

    async def run(self, code: str, stdin: str):
        # Write code to a temp file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as src:
            src.write(code.encode())
            src_path = src.name

        try:
            # Invoke the appropriate python interpreter
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
