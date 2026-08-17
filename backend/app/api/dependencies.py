from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.users import get_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не удалось подтвердить учётные данные.",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        subject = decode_access_token(token)
        user_id = int(subject)
    except (jwt.PyJWTError, ValueError):
        raise CredentialsException from None

    user = get_by_id(db, user_id)
    if user is None:
        raise CredentialsException
    return user
