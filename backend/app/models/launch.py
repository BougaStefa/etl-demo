from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# base model
class LaunchBase(BaseModel):
    """Base model for SpaceX launch data"""

    name: str = Field(..., description="Name of the launch mission")
    flight_number: int = Field(..., description="Flight number of the launch")
    date_utc: datetime = Field(..., description="UTC date and time of the launch")
    success: Optional[bool] = Field(
        None, description="Whether the launch was successful"
    )
    details: Optional[str] = Field(
        None, description="Detailed description of the launch"
    )
    rocket_id: Optional[str] = Field(
        None, description="ID of the rocket used in the launch"
    )


# new launch model, inherits all from base
class LaunchCreate(LaunchBase):
    """Model for creating a new launch record"""

    pass


# response model, includres base plus metadata
class Launch(LaunchBase):
    """Model for launch response data"""

    id: str = Field(..., description="Unique identifier for the launch")
    created_at: Optional[datetime] = Field(
        None, description="Timestamp when the record was created"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp when the record was last updated"
    )

    class Config:
        from_attributes = True  # to convert from SQLAlchemy to Pydantic
