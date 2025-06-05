from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# load .env variables
load_dotenv()

# env url
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# create engine with connection string
engine = create_engine(DATABASE_URL)
# factory for creating db sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# base class for models
Base = declarative_base()

# Define LaunchData model
class LaunchData(Base):
    __tablename__ = "launches"

    id = Column(String, primary_key=True)
    name = Column(String)
    flight_number = Column(Integer)
    date_utc = Column(DateTime)
    success = Column(Boolean, nullable=True)
    details = Column(String, nullable=True)
    rocket_id = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

def create_tables():
    # creates the tables if they dont exist
    Base.metadata.create_all(bind=engine)

# db session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
