import uuid

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.core.database import SessionLocal
from app.main import app
from app.models.user import User


client = TestClient(app)


def test_custom_itinerary_item_can_be_renamed_but_not_emptied() -> None:
    email = f"custom-item-{uuid.uuid4().hex}@example.com"
    try:
        client.post("/api/v1/auth/register", json={"full_name": "Custom Tester", "email": email, "password": "secure-password-123"})
        token = client.post("/api/v1/auth/login", json={"email": email, "password": "secure-password-123"}).json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        city_id = client.get("/api/v1/cities").json()[0]["id"]
        trip = client.post("/api/v1/trips", headers=headers, json={"city_id": city_id, "title": "Custom trip", "start_date": "2026-09-01", "end_date": "2026-09-01"}).json()
        day = trip["days"][0]
        item = client.post(f"/api/v1/trips/{trip['id']}/days/{day['id']}/items", headers=headers, json={"custom_title": "Coffee near hotel", "start_time": "09:00"}).json()

        updated = client.put(f"/api/v1/trips/{trip['id']}/days/{day['id']}/items/{item['id']}", headers=headers, json={"custom_title": "Meet friends", "start_time": "11:30"})
        assert updated.status_code == 200
        assert updated.json()["custom_title"] == "Meet friends"
        assert updated.json()["start_time"] == "11:30:00"
        assert client.put(f"/api/v1/trips/{trip['id']}/days/{day['id']}/items/{item['id']}", headers=headers, json={"custom_title": "   "}).status_code == 422
    finally:
        with SessionLocal() as db:
            db.execute(delete(User).where(User.email == email))
            db.commit()
