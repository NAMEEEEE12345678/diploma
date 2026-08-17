import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


class WeatherUnavailableError(Exception):
    """The external weather provider did not return usable data."""


WEATHER_CONDITIONS = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Облачно",
    45: "Туман",
    48: "Изморозь",
    51: "Лёгкая морось",
    53: "Морось",
    55: "Сильная морось",
    61: "Небольшой дождь",
    63: "Дождь",
    65: "Сильный дождь",
    71: "Небольшой снег",
    73: "Снег",
    75: "Сильный снег",
    80: "Ливень",
    81: "Ливень",
    82: "Сильный ливень",
    95: "Гроза",
    96: "Гроза с градом",
    99: "Сильная гроза с градом",
}


def condition_for(code: int) -> str:
    return WEATHER_CONDITIONS.get(code, "Переменная погода")


def fetch_weather(latitude: float, longitude: float) -> dict[str, Any]:
    query = urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_min,temperature_2m_max",
        "forecast_days": 5,
        "timezone": "auto",
        "wind_speed_unit": "ms",
    })
    try:
        with urlopen(f"https://api.open-meteo.com/v1/forecast?{query}", timeout=8) as response:
            payload = json.load(response)
    except (HTTPError, URLError, OSError, TimeoutError, json.JSONDecodeError) as error:
        raise WeatherUnavailableError from error

    if not isinstance(payload, dict) or "current" not in payload or "daily" not in payload:
        raise WeatherUnavailableError
    return payload
