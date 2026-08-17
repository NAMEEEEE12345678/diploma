from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.favorites import router as favorites_router
from app.api.v1.health import router as health_router
from app.api.v1.users import router as users_router
from app.api.v1.trips import router as trips_router
from app.api.v1.checklist import router as checklist_router
from app.api.v1.weather import router as weather_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(catalog_router)
api_router.include_router(trips_router)
api_router.include_router(favorites_router)
api_router.include_router(checklist_router)
api_router.include_router(weather_router)
