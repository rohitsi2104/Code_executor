import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_pyspark_execution():
    response = client.post(
        "/api/v1/execute",
        json={
            "language": "pyspark",
            "version": "3.1",
            "code": "print('Hello, PySpark!')"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert "Hello, PySpark!" in body["stdout"]
