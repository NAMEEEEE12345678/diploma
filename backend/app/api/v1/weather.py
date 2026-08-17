from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.city import City
from app.models.place import Place
from app.schemas.weather import CityWeatherRead, CurrentWeatherRead, ForecastDayRead
from app.services.weather import WeatherUnavailableError, condition_for, fetch_weather

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("", response_model=CityWeatherRead)
def read_weather(city_id: int, db: Annotated[Session, Depends(get_db)]) -> CityWeatherRead:
    city = db.get(City, city_id)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Город не найден.")

    latitude, longitude = db.execute(
        select(func.avg(Place.latitude), func.avg(Place.longitude)).where(Place.city_id == city_id)
    ).one()
    if latitude is None or longitude is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Для города нет координат.")

    try:
        weather = fetch_weather(float(latitude), float(longitude))
        current = weather["current"]
        daily = weather["daily"]
        weather_code = int(current["weather_code"])
        forecast = [
            ForecastDayRead(
                date=day,
                weather_code=int(code),
                condition=condition_for(int(code)),
                temperature_min=round(float(minimum), 1),
                temperature_max=round(float(maximum), 1),
            )
            for day, code, minimum, maximum in zip(
                daily["time"], daily["weather_code"], daily["temperature_2m_min"], daily["temperature_2m_max"], strict=True
            )
        ]
    except (KeyError, TypeError, ValueError, WeatherUnavailableError):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Не удалось загрузить погоду. Попробуйте позже.") from None

    return CityWeatherRead(
        city_id=city.id,
        city_name=city.name,
        current=CurrentWeatherRead(
            temperature=round(float(current["temperature_2m"]), 1),
            apparent_temperature=round(float(current["apparent_temperature"]), 1),
            condition=condition_for(weather_code),
            weather_code=weather_code,
            humidity=int(current["relative_humidity_2m"]),
            wind_speed=round(float(current["wind_speed_10m"]), 1),
            temperature_min=round(float(daily["temperature_2m_min"][0]), 1),
            temperature_max=round(float(daily["temperature_2m_max"][0]), 1),
        ),
        forecast=forecast,
    )
