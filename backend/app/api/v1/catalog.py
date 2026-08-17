from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories import catalog as catalog_repository
from app.schemas.catalog import CityRead, CountryRead, PlaceRead

router = APIRouter(tags=["Каталог направлений"])


def get_or_404(resource: object | None, resource_name: str) -> object:
    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} не найден.",
        )
    return resource


@router.get("/countries", response_model=list[CountryRead])
def read_countries(db: Annotated[Session, Depends(get_db)]) -> list[CountryRead]:
    return catalog_repository.get_countries(db)


@router.get("/countries/{country_id}", response_model=CountryRead)
def read_country(
    country_id: int, db: Annotated[Session, Depends(get_db)]
) -> CountryRead:
    return get_or_404(catalog_repository.get_country(db, country_id), "Страна")  # type: ignore[return-value]


@router.get("/cities", response_model=list[CityRead])
def read_cities(
    db: Annotated[Session, Depends(get_db)],
    country_id: int | None = Query(default=None),
) -> list[CityRead]:
    return catalog_repository.get_cities(db, country_id)


@router.get("/cities/{city_id}", response_model=CityRead)
def read_city(city_id: int, db: Annotated[Session, Depends(get_db)]) -> CityRead:
    return get_or_404(catalog_repository.get_city(db, city_id), "Город")  # type: ignore[return-value]


@router.get("/cities/{city_id}/places", response_model=list[PlaceRead])
def read_city_places(
    city_id: int, db: Annotated[Session, Depends(get_db)]
) -> list[PlaceRead]:
    get_or_404(catalog_repository.get_city(db, city_id), "Город")
    return catalog_repository.get_places(db, city_id)


@router.get("/places", response_model=list[PlaceRead])
def read_places(
    db: Annotated[Session, Depends(get_db)],
    city_id: int | None = Query(default=None),
) -> list[PlaceRead]:
    return catalog_repository.get_places(db, city_id)


@router.get("/places/{place_id}", response_model=PlaceRead)
def read_place(place_id: int, db: Annotated[Session, Depends(get_db)]) -> PlaceRead:
    return get_or_404(catalog_repository.get_place(db, place_id), "Место")  # type: ignore[return-value]
