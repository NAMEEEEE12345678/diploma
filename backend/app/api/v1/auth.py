from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.users import get_by_email
from app.schemas.auth import Token, UserLogin, UserRead, UserRegister

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: UserRegister, db: Annotated[Session, Depends(get_db)]
) -> User:
    email = str(payload.email).lower()
    if get_by_email(db, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует.",
        )

    user = User(
        full_name=payload.full_name.strip(),
        email=email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует.",
        ) from None
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login_user(
    payload: UserLogin, db: Annotated[Session, Depends(get_db)]
) -> Token:
    user = get_by_email(db, str(payload.email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=create_access_token(str(user.id)))
