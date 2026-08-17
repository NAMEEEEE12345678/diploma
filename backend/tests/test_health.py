from fastapi.testclient import TestClient

from app.main import app


def test_root_returns_welcome_message() -> None:
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "API конструктора путешествий работает"


def test_health_reports_database_connection() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}
