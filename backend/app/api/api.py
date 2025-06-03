from fastapi import APIRouter
from .routes import launches

api_router = APIRouter()
api_router.include_router(launches.router, prefix="/launches",tags = ["launches"])
