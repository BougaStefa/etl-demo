from fastapi import APIRouter
from api.routes import launches, auth,bookmarks

api_router = APIRouter()
api_router.include_router(launches.router, prefix="/launches",tags = ["launches"])
api_router.include_router(bookmarks.router, prefix="/bookmarks",tags = ["bookmarks"])
api_router.include_router(auth.router, tags = ["auth"])
