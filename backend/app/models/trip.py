from __future__ import annotations
from datetime import date, datetime, time
from typing import TYPE_CHECKING
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.city import City
    from app.models.place import Place
class Trip(Base):
    __tablename__="trips"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    city_id: Mapped[int]=mapped_column(ForeignKey("cities.id"), index=True)
    title: Mapped[str]=mapped_column(String(180))
    start_date: Mapped[date]=mapped_column(Date)
    end_date: Mapped[date]=mapped_column(Date)
    budget: Mapped[float|None]=mapped_column(Numeric(12,2), nullable=True)
    description: Mapped[str|None]=mapped_column(Text, nullable=True)
    interests: Mapped[list[str]] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user: Mapped[User]=relationship(back_populates="trips")
    city: Mapped[City]=relationship(back_populates="trips")
    days: Mapped[list[TripDay]]=relationship(back_populates="trip", cascade="all, delete-orphan", order_by="TripDay.day_number")
class TripDay(Base):
    __tablename__="trip_days"
    __table_args__=(UniqueConstraint("trip_id","day_number",name="uq_trip_days_number"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    trip_id: Mapped[int]=mapped_column(ForeignKey("trips.id", ondelete="CASCADE"), index=True)
    day_number: Mapped[int]=mapped_column(Integer)
    date: Mapped[date]=mapped_column(Date)
    trip: Mapped[Trip]=relationship(back_populates="days")
    items: Mapped[list[ItineraryItem]]=relationship(back_populates="trip_day", cascade="all, delete-orphan", order_by="ItineraryItem.position")
class ItineraryItem(Base):
    __tablename__="itinerary_items"
    __table_args__=(UniqueConstraint("trip_day_id","position",name="uq_itinerary_item_position"),)
    id: Mapped[int]=mapped_column(primary_key=True)
    trip_day_id: Mapped[int]=mapped_column(ForeignKey("trip_days.id", ondelete="CASCADE"), index=True)
    place_id: Mapped[int|None]=mapped_column(ForeignKey("places.id"), nullable=True)
    custom_title: Mapped[str|None]=mapped_column(String(180), nullable=True)
    start_time: Mapped[time|None]=mapped_column(Time, nullable=True)
    note: Mapped[str|None]=mapped_column(Text, nullable=True)
    position: Mapped[int]=mapped_column(Integer)
    trip_day: Mapped[TripDay]=relationship(back_populates="items")
    place: Mapped[Place|None]=relationship(back_populates="itinerary_items")
