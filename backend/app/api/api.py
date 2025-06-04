from fastapi import APIRouter
from api.routes import launches, auth

api_router = APIRouter()
api_router.include_router(launches.router, prefix="/launches",tags = ["launches"])
api_router.include_router(auth.router, tags = ["auth"])
