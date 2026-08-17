from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.city import City
from app.models.country import Country
from app.models.place import Place


def get_countries(db: Session) -> list[Country]:
    return list(db.scalars(select(Country).order_by(Country.name)))


def get_country(db: Session, country_id: int) -> Country | None:
    return db.get(Country, country_id)


def get_cities(db: Session, country_id: int | None = None) -> list[City]:
    statement = select(City).order_by(City.name)
    if country_id is not None:
        statement = statement.where(City.country_id == country_id)
    return list(db.scalars(statement))


def get_city(db: Session, city_id: int) -> City | None:
    return db.get(City, city_id)


def get_places(db: Session, city_id: int | None = None) -> list[Place]:
    statement = select(Place).order_by(Place.name)
    if city_id is not None:
        statement = statement.where(Place.city_id == city_id)
    return list(db.scalars(statement))


def get_place(db: Session, place_id: int) -> Place | None:
    return db.get(Place, place_id)
