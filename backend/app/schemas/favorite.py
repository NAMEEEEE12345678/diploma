from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.catalog import PlaceRead
class FavoriteRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int
    place_id:int
    created_at:datetime
    place:PlaceRead
