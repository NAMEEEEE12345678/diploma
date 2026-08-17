from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update as sqlalchemy_update
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.checklist import ChecklistItem
from app.models.user import User
from app.schemas.checklist import ChecklistCreate, ChecklistRead, ChecklistUpdate

router = APIRouter(prefix="/checklist", tags=["Checklist"])


@router.get("", response_model=list[ChecklistRead])
def items(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    return list(db.scalars(select(ChecklistItem).where(ChecklistItem.user_id == user.id)))


@router.post("", response_model=ChecklistRead, status_code=status.HTTP_201_CREATED)
def add(payload: ChecklistCreate, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    if not payload.base_key and not (payload.title or "").strip():
        raise HTTPException(422, "Укажите название пункта.")
    item = db.scalar(select(ChecklistItem).where(ChecklistItem.user_id == user.id, ChecklistItem.base_key == payload.base_key)) if payload.base_key else None
    if item:
        return item
    item = ChecklistItem(user_id=user.id, title=payload.title.strip() if payload.title else None, base_key=payload.base_key)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/checks", status_code=204)
def reset(db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    db.execute(sqlalchemy_update(ChecklistItem).where(ChecklistItem.user_id == user.id).values(checked=False))
    db.commit()


@router.put("/{item_id}", response_model=ChecklistRead)
def update(item_id: int, payload: ChecklistUpdate, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    item = db.scalar(select(ChecklistItem).where(ChecklistItem.id == item_id, ChecklistItem.user_id == user.id))
    if not item:
        raise HTTPException(404, "Пункт чек-листа не найден.")
    item.checked = payload.checked
    db.commit()
    return item


@router.delete("/{item_id}", status_code=204)
def remove(item_id: int, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user)]):
    item = db.scalar(select(ChecklistItem).where(ChecklistItem.id == item_id, ChecklistItem.user_id == user.id, ChecklistItem.base_key.is_(None)))
    if not item:
        raise HTTPException(404, "Пункт чек-листа не найден.")
    db.delete(item)
    db.commit()
