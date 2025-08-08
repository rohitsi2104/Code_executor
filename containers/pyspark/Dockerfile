# containers/pyspark/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# spark needs a JVM for some features; lightweight JRE helps
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
  && rm -rf /var/lib/apt/lists/*

# minimal deps for the runner API + pyspark (local[*])
RUN pip install --no-cache-dir fastapi uvicorn pydantic pyspark==3.5.1

WORKDIR /app
# just copy the runner file, not the whole repo
COPY containers/pyspark/runner_service.py /app/runner_service.py

EXPOSE 8080
CMD ["uvicorn", "runner_service:app", "--host", "0.0.0.0", "--port", "8080"]
