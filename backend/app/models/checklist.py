from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
class ChecklistItem(Base):
    __tablename__='checklist_items'; __table_args__=(UniqueConstraint('user_id','base_key',name='uq_checklist_base'),)
    id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    base_key:Mapped[str|None]=mapped_column(String(80),nullable=True); title:Mapped[str|None]=mapped_column(String(180),nullable=True)
    checked:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
