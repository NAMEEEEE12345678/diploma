from datetime import date, datetime, time
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.schemas.catalog import CityRead, PlaceRead
class TripCreate(BaseModel):
    city_id:int
    title:str=Field(min_length=2,max_length=180)
    start_date:date
    end_date:date
    budget:float|None=Field(default=None,ge=0)
    description:str|None=Field(default=None,max_length=3000)
    interests:list[str]=Field(default_factory=list)
    @model_validator(mode="after")
    def dates_valid(self):
        if self.end_date < self.start_date: raise ValueError("Дата окончания не может быть раньше даты начала.")
        return self
class TripUpdate(TripCreate): pass
class DayCreate(BaseModel):
    day_number:int=Field(ge=1)
    date:date
class ItemCreate(BaseModel):
    place_id:int|None=None
    custom_title:str|None=Field(default=None,min_length=1,max_length=180)
    start_time:time|None=None
    note:str|None=Field(default=None,max_length=1000)
    position:int|None=Field(default=None,ge=1)
    @model_validator(mode="after")
    def place_or_custom_title(self):
        if self.place_id is None and not (self.custom_title or "").strip(): raise ValueError("Укажите место из каталога или название своего места.")
        if self.place_id is not None and (self.custom_title or "").strip(): raise ValueError("Можно указать только один тип места.")
        self.custom_title=self.custom_title.strip() if self.custom_title else None
        return self
class ItemUpdate(BaseModel):
    custom_title:str|None=Field(default=None,max_length=180)
    start_time:time|None=None
    note:str|None=Field(default=None,max_length=1000)
    position:int|None=Field(default=None,ge=1)
class ItemRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; trip_day_id:int; place_id:int|None; custom_title:str|None; start_time:time|None; note:str|None; position:int; place:PlaceRead|None
class DayRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; trip_id:int; day_number:int; date:date; items:list[ItemRead]=[]
class TripRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; user_id:int; city_id:int; title:str; start_date:date; end_date:date; budget:float|None; description:str|None; interests:list[str]; created_at:datetime; updated_at:datetime; city:CityRead; days:list[DayRead]=[]
