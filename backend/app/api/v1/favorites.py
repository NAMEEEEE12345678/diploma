from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.favorite import Favorite
from app.models.place import Place
from app.models.user import User
from app.schemas.favorite import FavoriteRead
router=APIRouter(prefix="/favorites",tags=["Избранное"])
@router.get("",response_model=list[FavoriteRead])
def list_favorites(db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    return list(db.scalars(select(Favorite).options(selectinload(Favorite.place)).where(Favorite.user_id==user.id).order_by(Favorite.created_at.desc())))
@router.post("/{place_id}",response_model=FavoriteRead,status_code=status.HTTP_201_CREATED)
def add_favorite(place_id:int,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    if not db.get(Place,place_id): raise HTTPException(404,"Место не найдено.")
    favorite=Favorite(user_id=user.id,place_id=place_id);db.add(favorite)
    try: db.commit()
    except IntegrityError: db.rollback();raise HTTPException(409,"Место уже в избранном.") from None
    return db.scalar(select(Favorite).options(selectinload(Favorite.place)).where(Favorite.id==favorite.id))
@router.delete("/{place_id}",status_code=204)
def remove_favorite(place_id:int,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    favorite=db.scalar(select(Favorite).where(Favorite.user_id==user.id,Favorite.place_id==place_id))
    if not favorite: raise HTTPException(404,"Место не найдено в избранном.")
    db.delete(favorite);db.commit()
