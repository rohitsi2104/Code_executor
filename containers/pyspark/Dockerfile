FROM bitnami/spark:latest

WORKDIR /app

USER root
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir fastapi uvicorn fastapi-mcp==0.4.0
    

COPY . /app

USER 1001

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
