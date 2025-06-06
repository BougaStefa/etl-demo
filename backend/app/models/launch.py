from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# base model
class LaunchBase(BaseModel):
    name: str
    flight_number: int
    date_utc: datetime
    success: Optional[bool] = None
    details: Optional[str] = None
    rocket_id: Optional[str] = None

# new launch model, inherits all from base
class LaunchCreate(LaunchBase):
    pass

# response model, includres base plus metadata
class Launch(LaunchBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # to convert from SQLAlchemy to Pydantic
