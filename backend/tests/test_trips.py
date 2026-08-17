import uuid
from fastapi.testclient import TestClient
from sqlalchemy import delete
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
client=TestClient(app)
def token(email):
    client.post("/api/v1/auth/register",json={"full_name":"Trip Tester","email":email,"password":"secure-password-123"})
    return client.post("/api/v1/auth/login",json={"email":email,"password":"secure-password-123"}).json()["access_token"]
def test_trip_crud_and_ownership():
    suffix=uuid.uuid4().hex; a=f"trip-a-{suffix}@example.com"; b=f"trip-b-{suffix}@example.com"
    try:
        headers={"Authorization":f"Bearer {token(a)}"}; other={"Authorization":f"Bearer {token(b)}"}
        city=client.get("/api/v1/cities").json()[0]; place=client.get(f"/api/v1/cities/{city['id']}/places").json()[0]
        created=client.post("/api/v1/trips",headers=headers,json={"city_id":city["id"],"title":"Тестовая поездка","start_date":"2026-09-01","end_date":"2026-09-02","budget":100}).json()
        assert len(created["days"])==2
        assert client.get(f"/api/v1/trips/{created['id']}",headers=other).status_code==404
        item=client.post(f"/api/v1/trips/{created['id']}/days/{created['days'][0]['id']}/items",headers=headers,json={"place_id":place["id"]}).json()
        assert client.put(f"/api/v1/trips/{created['id']}",headers=headers,json={"city_id":city["id"],"title":"Обновлено","start_date":"2026-09-01","end_date":"2026-09-02","budget":200}).json()["title"]=="Обновлено"
        assert client.delete(f"/api/v1/trips/{created['id']}/days/{created['days'][0]['id']}/items/{item['id']}",headers=headers).status_code==204
        assert client.delete(f"/api/v1/trips/{created['id']}",headers=headers).status_code==204
    finally:
        with SessionLocal() as db: db.execute(delete(User).where(User.email.in_([a,b]))); db.commit()
