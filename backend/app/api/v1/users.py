from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import UserRead

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user
