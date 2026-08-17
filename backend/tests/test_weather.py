from fastapi.testclient import TestClient

from app.api.v1 import weather as weather_api
from app.main import app


def test_weather_endpoint_returns_current_conditions_and_forecast(monkeypatch) -> None:
    monkeypatch.setattr(weather_api, "fetch_weather", lambda latitude, longitude: {
        "current": {
            "temperature_2m": 24.2,
            "apparent_temperature": 23.1,
            "relative_humidity_2m": 48,
            "weather_code": 3,
            "wind_speed_10m": 3.2,
        },
        "daily": {
            "time": ["2026-08-17", "2026-08-18"],
            "weather_code": [3, 61],
            "temperature_2m_min": [18.2, 17.5],
            "temperature_2m_max": [26.4, 23.8],
        },
    })
    client = TestClient(app)
    city_id = client.get("/api/v1/cities").json()[0]["id"]

    response = client.get("/api/v1/weather", params={"city_id": city_id})

    assert response.status_code == 200
    payload = response.json()
    assert payload["city_id"] == city_id
    assert payload["current"]["temperature"] == 24.2
    assert payload["current"]["condition"] == "Облачно"
    assert len(payload["forecast"]) == 2
    assert payload["forecast"][1]["condition"] == "Небольшой дождь"


def test_weather_endpoint_returns_404_for_unknown_city() -> None:
    response = TestClient(app).get("/api/v1/weather", params={"city_id": 999999})
    assert response.status_code == 404
