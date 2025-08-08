# from executor.pyspark_runner import PySparkRunner
# from executor.python_runner import PythonRunner

# # Map (language, version) → runner instance
# RUNTIMES = {
#     ("pyspark", "3.1"):      PySparkRunner(),
#     ("python",  "3.10.0"):   PythonRunner('3.10.0'),
#     ("python",  "3.11.0"):   PythonRunner('3.11.0'),
# }

# def get_runner(language: str, version: str):
#     """
#     Fetch the runner for a given language/version tuple.
#     Raises KeyError if unsupported.
#     """
#     key = (language.lower(), version)
#     if key not in RUNTIMES:
#         raise ValueError(f"Unsupported language/version: {language} {version}")
#     return RUNTIMES[key]


from executor.pyspark_runner import PySparkRunner
from executor.python_runner import PythonRunner

def normalize_version(lang: str, version: str) -> str:
    v = version.strip()
    if lang.lower() == "python":
        # Accept 3.10 or 3.10.0 => normalize to 3.10.0
        parts = v.split(".")
        if len(parts) == 2:
            return f"{parts[0]}.{parts[1]}.0"
    return v

def get_runner(language: str, version: str):
    lang = language.lower()
    v = normalize_version(lang, version)

    if lang == "python":
        return PythonRunner(v)
    if lang == "pyspark":
        return PySparkRunner(v)

    raise ValueError(f"Unsupported language/version: {language} {version}")
