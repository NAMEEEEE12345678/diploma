from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
class Favorite(Base):
    __tablename__="favorites"
    __table_args__=(UniqueConstraint("user_id","place_id",name="uq_favorites_user_place"),)
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True)
    place_id:Mapped[int]=mapped_column(ForeignKey("places.id",ondelete="CASCADE"),index=True)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    user=relationship("User")
    place=relationship("Place")
