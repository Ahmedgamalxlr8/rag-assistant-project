import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_health_endpoint():
    """Confirms GET /health returns 200 with vector store chunks loaded."""
    with TestClient(app) as tc:
        response = tc.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["chunks_indexed"] > 0

def test_query_happy_path():
    """Confirms POST /query responds with an answer and citations."""
    with TestClient(app) as tc:
        payload = {"question": "What is the policy on jury service?"}
        response = tc.post("/query", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert isinstance(data["sources"], list)
        assert len(data["sources"]) > 0

def test_query_invalid_input_validation():
    """Confirms sending an invalid short question returns HTTP 422."""
    with TestClient(app) as tc:
        # question is shorter than min_length=3
        response = tc.post("/query", json={"question": "a"})
        assert response.status_code == 422