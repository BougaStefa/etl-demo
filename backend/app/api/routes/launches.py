from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...core.deps import get_current_user
from ...database import get_db, LaunchData
from ...models.launch import Launch, LaunchCreate

router = APIRouter()

@router.get("/", response_model=List[Launch])
def get_all_launches(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    launches = db.query(LaunchData).all()
    return launches

@router.get("/{launch_id}", response_model=Launch)
def get_launch(
    launch_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    launch = db.query(LaunchData).filter(LaunchData.id == launch_id).first()
    if not launch:
        raise HTTPException(status_code=404, detail="Launch not found")
    return launch
