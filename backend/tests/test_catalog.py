from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_catalog_endpoints_return_seeded_data() -> None:
    countries = client.get("/api/v1/countries")
    assert countries.status_code == 200
    assert len(countries.json()) >= 3

    country = countries.json()[0]
    country_response = client.get(f"/api/v1/countries/{country['id']}")
    assert country_response.status_code == 200
    assert country_response.json()["code"] == country["code"]

    cities = client.get("/api/v1/cities")
    assert cities.status_code == 200
    assert len(cities.json()) >= 3

    city = cities.json()[0]
    assert client.get(f"/api/v1/cities/{city['id']}").status_code == 200

    city_places = client.get(f"/api/v1/cities/{city['id']}/places")
    assert city_places.status_code == 200
    assert len(city_places.json()) >= 1

    places = client.get("/api/v1/places")
    assert places.status_code == 200
    place = places.json()[0]
    assert client.get(f"/api/v1/places/{place['id']}").status_code == 200


def test_catalog_returns_404_for_unknown_resources() -> None:
    response = client.get("/api/v1/countries/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Страна не найден."
