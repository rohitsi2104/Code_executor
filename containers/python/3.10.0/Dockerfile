FROM python:3.10.0-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY containers/python/3.10.0/runner_service.py /app/runner_service.py
EXPOSE 8080
CMD ["uvicorn", "runner_service:app", "--host", "0.0.0.0", "--port", "8080"]
