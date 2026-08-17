import uuid
from fastapi.testclient import TestClient
from sqlalchemy import delete
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
client=TestClient(app)
def token(email):
 client.post("/api/v1/auth/register",json={"full_name":"Favorite Tester","email":email,"password":"secure-password-123"})
 return {"Authorization":"Bearer "+client.post("/api/v1/auth/login",json={"email":email,"password":"secure-password-123"}).json()["access_token"]}
def test_favorites_are_unique_and_private():
 a=f"fav-a-{uuid.uuid4().hex}@example.com";b=f"fav-b-{uuid.uuid4().hex}@example.com"
 try:
  ah,bh=token(a),token(b);place=client.get("/api/v1/places").json()[0]["id"]
  assert client.post(f"/api/v1/favorites/{place}",headers=ah).status_code==201
  assert client.post(f"/api/v1/favorites/{place}",headers=ah).status_code==409
  assert len(client.get("/api/v1/favorites",headers=ah).json())==1
  assert client.get("/api/v1/favorites",headers=bh).json()==[]
  assert client.delete(f"/api/v1/favorites/{place}",headers=ah).status_code==204
 finally:
  with SessionLocal() as db: db.execute(delete(User).where(User.email.in_([a,b])));db.commit()
