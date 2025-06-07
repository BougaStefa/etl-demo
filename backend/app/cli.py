import asyncio
from database import SessionLocal, create_tables
from etl.manager import ETLManager

def main():
    # Create tables
    create_tables()

    db = SessionLocal()

    # Run pipeline to fetch and store SpaceX launch data
    try:
        etl_manager = ETLManager(db)
        count = asyncio.run(etl_manager.run_etl())
        print(f"Successfully processed {count} launches")
    finally:
        db.close()

if __name__ == "__main__":
    main()
