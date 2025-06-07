import asyncio
import logging
from app.database import SessionLocal
from app.etl.manager import ETLManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def run_etl():
    """Run ETL process"""
    session = SessionLocal()
    try:
        manager = ETLManager(session)
        await manager.execute_etl()
    finally:
        session.close()

if __name__ == "__main__":
    asyncio.run(run_etl())
