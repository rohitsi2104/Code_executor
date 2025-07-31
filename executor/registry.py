from executor.pyspark_runner import PySparkRunner
from executor.python_runner import PythonRunner

# Map (language, version) → runner instance
RUNTIMES = {
    ("pyspark", "3.1"):      PySparkRunner(),
    ("python",  "3.10.0"):   PythonRunner(),
    ("python",  "3.11.0"):   PythonRunner(),
}

def get_runner(language: str, version: str):
    """
    Fetch the runner for a given language/version tuple.
    Raises KeyError if unsupported.
    """
    key = (language.lower(), version)
    if key not in RUNTIMES:
        raise ValueError(f"Unsupported language/version: {language} {version}")
    return RUNTIMES[key]
