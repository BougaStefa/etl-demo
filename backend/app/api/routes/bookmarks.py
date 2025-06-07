from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, LaunchBookmark, LaunchData
from app.models.bookmark import BookmarkCreate, Bookmark
from app.core.deps import get_current_user_id

router = APIRouter()

@router.post("/", response_model=Bookmark, status_code=status.HTTP_201_CREATED)
def create_bookmark(
    bookmark: BookmarkCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Check if launch exists
    launch = db.query(LaunchData).filter(LaunchData.id == bookmark.launch_id).first()
    if not launch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Launch not found"
        )
    
    # Check if bookmark already exists
    existing_bookmark = db.query(LaunchBookmark).filter(
        LaunchBookmark.user_id == user_id,  
        LaunchBookmark.launch_id == bookmark.launch_id
    ).first()
    
    if existing_bookmark:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Launch already bookmarked"
        )
    
    # Create new bookmark
    db_bookmark = LaunchBookmark(
        user_id=user_id,
        launch_id=bookmark.launch_id
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark

@router.get("/", response_model=List[Bookmark])
def get_bookmarks(
    user_id: int = Depends(get_current_user_id), 
    db: Session = Depends(get_db)
):
    bookmarks = db.query(LaunchBookmark).filter(
        LaunchBookmark.user_id == user_id
    ).all()
    return bookmarks

@router.delete("/{launch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(
    launch_id: str,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    bookmark = db.query(LaunchBookmark).filter(
        LaunchBookmark.user_id == user_id,
        LaunchBookmark.launch_id == launch_id
    ).first()
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    db.delete(bookmark)
    db.commit()
    return None
