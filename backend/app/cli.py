import asyncio
import typer
from .database import SessionLocal, create_tables
from .etl.manager import ETLManager

app = typer.Typer()

@app.command()
def etl_command():
    # create tables
    create_tables()

    db = SessionLocal()

    # run pipeline to fetch and store SpaceX launch data
    try:
        etl_manager = ETLManager(db)
        count = asyncio.run(etl_manager.run_etl())
        typer.echo(f"Successfully processed {count} launches")
    finally:
        db.close()

def main():
    app()

if __name__ == "__main__":
    main()
