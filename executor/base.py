import abc

class CodeRunner(abc.ABC):
    @abc.abstractmethod
    async def run(self, code: str, stdin: str = None):
        """Run code and return output dict with keys: stdout, stderr, exit_code."""
        pass
