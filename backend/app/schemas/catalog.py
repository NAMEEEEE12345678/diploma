from pydantic import BaseModel, ConfigDict, Field


class CountryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str = Field(min_length=2, max_length=3)
    description: str
    image_url: str


class CityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    country_id: int
    name: str
    description: str
    image_url: str


class PlaceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    name: str
    description: str
    category: str
    image_url: str
    latitude: float
    longitude: float
    estimated_cost: float
    recommended_duration: int
