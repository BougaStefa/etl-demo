from fastapi import FastAPI, BackgroundTasks
from datetime import datetime, UTC
import logging
from app.etl.manager import ETLManager
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.database import create_tables, SessionLocal

create_tables()  # Ensure tables are created at startup

app = FastAPI(
    title="SpaceX API",
    description="""
    SpaceX Launch Tracker provides endpoints for managing SpaceX launch data, user authentication, and bookmarks.

    ## Features:

    * **Launches**: Access SpaceX launch data.
    * **Authentication**: User registration and JWT authentication.
    * **Bookmarks**: Save and manage user bookmarks for launches.
    * **ETL Pipeline**: Background ETL process to update launch data.

    ## Notes
    * All endpoints except registration and login require authentication via JWT.
    * Use the token endpoint to obtain a JWT token.
    * Include the token in the Authorization header as `Bearer <token>`
    """,
    version="1.0.0",
    contact={
        "name": "BougaStefa",
        "url": "https://github.com/BougaStefa/etl-demo",
    },
)
logger = logging.getLogger(__name__)


async def run_background_etl():
    """ETL process to run in background"""
    session = SessionLocal()
    try:
        manager = ETLManager(session)
        await manager.execute_etl()
    finally:
        session.close()


@app.post(
    "/etl/trigger",
    tags=["ETL"],
    summary="Trigger ETL Pipeline",
    description="""
    Trigger the ETL process to fetch latest SpaceX launch data.
    
    The process will:
    * Fetch latest launch data from SpaceX API
    * Transform the data to match our schema
    * Load the data into our database
    
    This is an asynchronous operation that runs in the background.
    """,
    responses={
        200: {
            "description": "ETL process started successfully",
            "content": {
                "application/json": {
                    "example": {"message": "ETL process started in background"}
                }
            },
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to start ETL process"}
                }
            },
        },
    },
)
async def trigger_etl(background_tasks: BackgroundTasks):
    """Endpoint to trigger ETL process in background"""
    background_tasks.add_task(run_background_etl)
    return {"message": "ETL process started in background"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://etl-demo.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
