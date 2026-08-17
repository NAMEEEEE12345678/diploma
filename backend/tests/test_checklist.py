import uuid

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.core.database import SessionLocal
from app.main import app
from app.models.user import User


client = TestClient(app)


def auth_headers(email: str) -> dict[str, str]:
    client.post("/api/v1/auth/register", json={"full_name": "Checklist Tester", "email": email, "password": "secure-password-123"})
    token = client.post("/api/v1/auth/login", json={"email": email, "password": "secure-password-123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_checklist_is_private_and_only_custom_items_can_be_deleted() -> None:
    suffix = uuid.uuid4().hex
    first_email, second_email = f"check-a-{suffix}@example.com", f"check-b-{suffix}@example.com"
    try:
        first, second = auth_headers(first_email), auth_headers(second_email)
        base = client.post("/api/v1/checklist", headers=first, json={"base_key": "documents-0"})
        assert base.status_code == 201
        base_id = base.json()["id"]
        assert client.put(f"/api/v1/checklist/{base_id}", headers=first, json={"checked": True}).json()["checked"] is True
        custom = client.post("/api/v1/checklist", headers=first, json={"title": "Camera"})
        assert custom.status_code == 201
        custom_id = custom.json()["id"]

        assert client.get("/api/v1/checklist", headers=second).json() == []
        assert client.delete(f"/api/v1/checklist/{base_id}", headers=first).status_code == 404
        assert client.delete("/api/v1/checklist/checks", headers=first).status_code == 204
        items = client.get("/api/v1/checklist", headers=first).json()
        assert len(items) == 2 and not any(item["checked"] for item in items)
        assert client.delete(f"/api/v1/checklist/{custom_id}", headers=first).status_code == 204
    finally:
        with SessionLocal() as db:
            db.execute(delete(User).where(User.email.in_([first_email, second_email])))
            db.commit()
