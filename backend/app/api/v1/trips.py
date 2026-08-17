from datetime import time, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload
from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.city import City
from app.models.place import Place
from app.models.trip import ItineraryItem, Trip, TripDay
from app.models.user import User
from app.schemas.trip import DayCreate, DayRead, ItemCreate, ItemRead, ItemUpdate, TripCreate, TripRead, TripUpdate

router=APIRouter(prefix="/trips",tags=["Путешествия"])
def trip_query(): return select(Trip).options(selectinload(Trip.city),selectinload(Trip.days).selectinload(TripDay.items).selectinload(ItineraryItem.place))
def owned(db,user,trip_id):
    trip=db.scalar(trip_query().where(Trip.id==trip_id,Trip.user_id==user.id))
    if not trip: raise HTTPException(404,"Путешествие не найдено.")
    return trip
@router.post("",response_model=TripRead,status_code=201)
def create(payload:TripCreate,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    if not db.get(City,payload.city_id): raise HTTPException(404,"Город не найден.")
    trip=Trip(user_id=user.id,**payload.model_dump()); db.add(trip); db.flush()
    for n in range((payload.end_date-payload.start_date).days+1): db.add(TripDay(trip_id=trip.id,day_number=n+1,date=payload.start_date+timedelta(days=n)))
    db.commit(); return owned(db,user,trip.id)
@router.get("",response_model=list[TripRead])
def list_trips(db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]): return list(db.scalars(trip_query().where(Trip.user_id==user.id).order_by(Trip.created_at.desc())))
@router.get("/{trip_id}",response_model=TripRead)
def get_trip(trip_id:int,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]): return owned(db,user,trip_id)
@router.put("/{trip_id}",response_model=TripRead)
def update(trip_id:int,payload:TripUpdate,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    trip=owned(db,user,trip_id)
    if not db.get(City,payload.city_id): raise HTTPException(404,"Город не найден.")
    for k,v in payload.model_dump().items(): setattr(trip,k,v)
    db.commit(); return owned(db,user,trip_id)
@router.delete("/{trip_id}",status_code=204)
def remove(trip_id:int,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]): db.delete(owned(db,user,trip_id)); db.commit()
@router.post("/{trip_id}/days",response_model=DayRead,status_code=201)
def add_day(trip_id:int,payload:DayCreate,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]): owned(db,user,trip_id); day=TripDay(trip_id=trip_id,**payload.model_dump()); db.add(day); db.commit(); db.refresh(day); return day
def owned_day(db,user,trip_id,day_id):
    owned(db,user,trip_id); day=db.scalar(select(TripDay).where(TripDay.id==day_id,TripDay.trip_id==trip_id))
    if not day: raise HTTPException(404,"День путешествия не найден.")
    return day
@router.post("/{trip_id}/days/{day_id}/items",response_model=ItemRead,status_code=201)
def add_item(trip_id:int,day_id:int,payload:ItemCreate,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    day=owned_day(db,user,trip_id,day_id); place=None
    if payload.place_id is not None:
        place=db.get(Place,payload.place_id)
        if not place or place.city_id!=owned(db,user,trip_id).city_id: raise HTTPException(400,"Место не относится к городу путешествия.")
    item=ItineraryItem(trip_day_id=day.id,place_id=place.id if place else None,custom_title=payload.custom_title,start_time=payload.start_time,note=payload.note,position=payload.position or len(day.items)+1); db.add(item); db.commit()
    return db.scalar(select(ItineraryItem).options(selectinload(ItineraryItem.place)).where(ItineraryItem.id==item.id))
@router.put("/{trip_id}/days/{day_id}/items/{item_id}",response_model=ItemRead)
def update_item(trip_id:int,day_id:int,item_id:int,payload:ItemUpdate,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    owned_day(db,user,trip_id,day_id); item=db.scalar(select(ItineraryItem).where(ItineraryItem.id==item_id,ItineraryItem.trip_day_id==day_id))
    if not item: raise HTTPException(404,"Элемент маршрута не найден.")
    updates=payload.model_dump(exclude_unset=True)
    if "custom_title" in updates:
        if item.place_id is not None: raise HTTPException(422,"Catalog place cannot become a custom place.")
        custom_title=(updates["custom_title"] or "").strip()
        if not custom_title: raise HTTPException(422,"Custom place title cannot be empty.")
        updates["custom_title"]=custom_title
    for k,v in updates.items(): setattr(item,k,v)
    db.commit(); return db.scalar(select(ItineraryItem).options(selectinload(ItineraryItem.place)).where(ItineraryItem.id==item.id))
@router.delete("/{trip_id}/days/{day_id}/items/{item_id}",status_code=204)
def delete_item(trip_id:int,day_id:int,item_id:int,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    owned_day(db,user,trip_id,day_id); item=db.scalar(select(ItineraryItem).where(ItineraryItem.id==item_id,ItineraryItem.trip_day_id==day_id))
    if not item: raise HTTPException(404,"Элемент маршрута не найден.")
    db.delete(item); db.commit()
@router.post("/{trip_id}/generate-itinerary",response_model=TripRead)
def generate_itinerary(trip_id:int,db:Annotated[Session,Depends(get_db)],user:Annotated[User,Depends(get_current_user)]):
    trip=owned(db,user,trip_id); category_map={"достопримечательности":{"История","Панорама","Прогулка"},"культура и музеи":{"История","Культура","Музей"},"природа":{"Природа"},"еда и кафе":{"Гастрономия","Еда"},"развлечения":{"Развлечения"},"шопинг":{"Шопинг"},"семейный отдых":{"Семейный отдых"}}
    requested=set().union(*(category_map.get(x.lower(),set()) for x in trip.interests)) if trip.interests else set(); places=list(db.scalars(select(Place).where(Place.city_id==trip.city_id))); candidates=sorted(places,key=lambda p:(p.category not in requested,p.id))
    db.execute(delete(ItineraryItem).where(ItineraryItem.trip_day_id.in_(select(TripDay.id).where(TripDay.trip_id==trip.id)),ItineraryItem.custom_title.is_(None)))
    selected=candidates
    state=[{"day":d,"minutes":0,"items":0} for d in trip.days]
    for p in selected:
        available=[s for s in state if s["items"]<4 and s["minutes"]+p.recommended_duration<=420]
        if not available: continue
        s=min(available,key=lambda x:(x["minutes"],x["items"])); start=540+s["minutes"]; db.add(ItineraryItem(trip_day_id=s["day"].id,place_id=p.id,position=s["items"]+1,start_time=time(start//60,start%60))); s["minutes"]+=p.recommended_duration; s["items"]+=1
    db.commit(); return owned(db,user,trip_id)
