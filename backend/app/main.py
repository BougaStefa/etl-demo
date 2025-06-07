from fastapi import FastAPI, BackgroundTasks
from datetime import datetime, UTC
import logging
from app.etl.manager import ETLManager
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.database import create_tables, SessionLocal

create_tables()  # Ensure tables are created at startup

app = FastAPI(title="SpaceX API")
logger = logging.getLogger(__name__)

async def run_background_etl():
    """ETL process to run in background"""
    session = SessionLocal()
    try:
        manager = ETLManager(session)
        await manager.execute_etl()
    finally:
        session.close()

@app.post("/etl/trigger")
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
