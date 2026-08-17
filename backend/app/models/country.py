from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.city import City


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    code: Mapped[str] = mapped_column(String(3), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(500))

    cities: Mapped[list[City]] = relationship(
        back_populates="country", cascade="all, delete-orphan"
    )
