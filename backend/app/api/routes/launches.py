from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_current_user
from app.database import get_db, LaunchData
from app.models.launch import Launch

router = APIRouter(
    tags=["Launches"],
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "Launch not found"},
    },
)


@router.get(
    "/",
    response_model=List[Launch],
    summary="Get all SpaceX launches",
    description="Retrieve all SpaceX launches from the database",
    responses={
        200: {
            "description": "List of all launches",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "5eb87cd9ffd86e000604b32a",
                            "name": "FalconSat",
                            "flight_number": 1,
                            "date_utc": "2006-03-24T22:30:00.000Z",
                            "success": False,
                        }
                    ]
                }
            },
        }
    },
)
def get_all_launches(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    launches = db.query(LaunchData).all()
    return launches


router.get(
    "/{launch_id}",
    response_model=Launch,
    summary="Get specific launch",
    description="Retrieve details of a specific SpaceX launch by ID",
    responses={
        200: {
            "description": "Launch details",
            "content": {
                "application/json": {
                    "example": {
                        "id": "5eb87cd9ffd86e000604b32a",
                        "name": "FalconSat",
                        "flight_number": 1,
                        "date_utc": "2006-03-24T22:30:00.000Z",
                        "success": False,
                    }
                }
            },
        }
    },
)


def get_launch(
    launch_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    launch = db.query(LaunchData).filter(LaunchData.id == launch_id).first()
    if not launch:
        raise HTTPException(status_code=404, detail="Launch not found")
    return launch
