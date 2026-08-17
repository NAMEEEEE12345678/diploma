from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.country import Country
    from app.models.place import Place
    from app.models.trip import Trip


class City(Base):
    __tablename__ = "cities"
    __table_args__ = (UniqueConstraint("country_id", "name", name="uq_cities_country_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(500))

    country: Mapped[Country] = relationship(back_populates="cities")
    places: Mapped[list[Place]] = relationship(
        back_populates="city", cascade="all, delete-orphan"
    )
    trips: Mapped[list[Trip]] = relationship(back_populates="city")
