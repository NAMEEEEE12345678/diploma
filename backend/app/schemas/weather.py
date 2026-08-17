from datetime import date

from pydantic import BaseModel


class CurrentWeatherRead(BaseModel):
    temperature: float
    apparent_temperature: float
    condition: str
    weather_code: int
    humidity: int
    wind_speed: float
    temperature_min: float
    temperature_max: float


class ForecastDayRead(BaseModel):
    date: date
    condition: str
    weather_code: int
    temperature_min: float
    temperature_max: float


class CityWeatherRead(BaseModel):
    city_id: int
    city_name: str
    current: CurrentWeatherRead
    forecast: list[ForecastDayRead]
