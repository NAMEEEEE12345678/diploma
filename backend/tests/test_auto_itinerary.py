import uuid
from fastapi.testclient import TestClient
from sqlalchemy import delete
from app.core.database import SessionLocal
from app.main import app
from app.models.user import User
client=TestClient(app)
def auth(email):
    client.post("/api/v1/auth/register",json={"full_name":"Auto Tester","email":email,"password":"secure-password-123"})
    return {"Authorization":"Bearer "+client.post("/api/v1/auth/login",json={"email":email,"password":"secure-password-123"}).json()["access_token"]}
def test_generate_itinerary_ignores_budget_and_keeps_ownership():
    suffix=uuid.uuid4().hex; a=f"auto-a-{suffix}@example.com"; b=f"auto-b-{suffix}@example.com"
    try:
        headers=auth(a); other=auth(b); city=client.get("/api/v1/cities").json()[0]
        trip=client.post("/api/v1/trips",headers=headers,json={"city_id":city["id"],"title":"Авто","start_date":"2026-10-01","end_date":"2026-10-03","budget":5000,"interests":["природа","культура и музеи"]}).json()
        generated=client.post(f"/api/v1/trips/{trip['id']}/generate-itinerary",headers=headers)
        assert generated.status_code==200
        data=generated.json(); items=[item for day in data["days"] for item in day["items"]]
        assert len({item["place_id"] for item in items})==len(items)
        assert items
        assert all(len(day["items"])<=4 for day in data["days"])
        assert client.post(f"/api/v1/trips/{trip['id']}/generate-itinerary",headers=other).status_code==404
        regenerated=client.post(f"/api/v1/trips/{trip['id']}/generate-itinerary",headers=headers).json()
        assert len({item["place_id"] for day in regenerated["days"] for item in day["items"]})==len([item for day in regenerated["days"] for item in day["items"]])
    finally:
        with SessionLocal() as db: db.execute(delete(User).where(User.email.in_([a,b])));db.commit()
