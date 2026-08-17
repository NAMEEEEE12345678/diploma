from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.city import City
    from app.models.trip import ItineraryItem


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(80), index=True)
    image_url: Mapped[str] = mapped_column(String(500))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    estimated_cost: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    recommended_duration: Mapped[int] = mapped_column()

    city: Mapped[City] = relationship(back_populates="places")
    itinerary_items: Mapped[list[ItineraryItem]] = relationship(back_populates="place")
