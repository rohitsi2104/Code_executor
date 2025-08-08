import httpx
from executor.base import CodeRunner

class PythonRunner(CodeRunner):
    def __init__(self, version: str):
        self.version = version

    def _service_name(self) -> str:
        # Expect versions like "3.10" or "3.10.0"
        parts = self.version.split(".")
        if len(parts) < 2:
            raise ValueError(f"Unsupported Python version format: {self.version}")
        return f"python{parts[0]}{parts[1]}"  # python310 or python311

    async def run(self, code: str, stdin: str = ""):
        url = f"http://{self._service_name()}:8080/execute"
        payload = {
            "language": "python",
            "version": self.version,
            "code": code,
            "stdin": stdin or ""
        }
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
