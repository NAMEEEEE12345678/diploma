import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.core.database import SessionLocal
from app.models.user import User
from app.main import app

client = TestClient(app)


@pytest.fixture
def user_email() -> str:
    email = f"test-auth-{uuid.uuid4().hex}@example.com"
    yield email
    with SessionLocal() as db:
        db.execute(delete(User).where(User.email == email))
        db.commit()


def test_registration_login_and_current_user(user_email: str) -> None:
    password = "secure-password-123"
    register = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Тестовый Пользователь", "email": user_email, "password": password},
    )

    assert register.status_code == 201
    registered_user = register.json()
    assert registered_user["email"] == user_email
    assert "password" not in registered_user
    assert "password_hash" not in registered_user

    with SessionLocal() as db:
        user = db.get(User, registered_user["id"])
        assert user is not None
        assert user.password_hash != password

    login = client.post(
        "/api/v1/auth/login", json={"email": user_email, "password": password}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    current_user = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert current_user.status_code == 200
    assert current_user.json()["id"] == registered_user["id"]


def test_registration_rejects_duplicate_email(user_email: str) -> None:
    payload = {"full_name": "Тестовый Пользователь", "email": user_email, "password": "secure-password-123"}

    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    duplicate = client.post("/api/v1/auth/register", json=payload)

    assert duplicate.status_code == 409
    assert duplicate.json()["detail"] == "Пользователь с таким email уже существует."


def test_private_endpoint_rejects_invalid_token() -> None:
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": "Bearer not-a-jwt"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Не удалось подтвердить учётные данные."


def test_registration_validates_input() -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "A", "email": "not-an-email", "password": "short"},
    )

    assert response.status_code == 422


def test_registration_rejects_blank_name() -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "  ",
            "email": "blank-name@example.com",
            "password": "secure-password-123",
        },
    )

    assert response.status_code == 422
