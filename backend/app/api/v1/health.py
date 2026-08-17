from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.health import HealthCheck

router = APIRouter(tags=["Состояние"])


@router.get("/health", response_model=HealthCheck)
def health_check(db: Session = Depends(get_db)) -> HealthCheck:
    db.execute(text("SELECT 1"))
    return HealthCheck(status="ok", database="connected")
