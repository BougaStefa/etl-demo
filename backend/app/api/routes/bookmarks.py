from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, LaunchBookmark, LaunchData
from app.models.bookmark import BookmarkCreate, Bookmark
from app.core.deps import get_current_user_id

router = APIRouter(
    tags=["Bookmarks"],
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "Resource not found"},
    },
)


@router.post(
    "/",
    response_model=Bookmark,
    status_code=status.HTTP_201_CREATED,
    summary="Create new bookmark",
    description="Create a new bookmark for a specific launch",
    responses={
        201: {
            "description": "Bookmark created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "launch_id": "5eb87cd9ffd86e000604b32a",
                        "created_at": "2025-06-08T12:12:43",
                    }
                }
            },
        },
        400: {
            "description": "Launch already bookmarked",
            "content": {
                "application/json": {"example": {"detail": "Launch already bookmarked"}}
            },
        },
    },
)
def create_bookmark(
    bookmark: BookmarkCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    # Check if launch exists
    launch = db.query(LaunchData).filter(LaunchData.id == bookmark.launch_id).first()
    if not launch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Launch not found"
        )

    # Check if bookmark already exists
    existing_bookmark = (
        db.query(LaunchBookmark)
        .filter(
            LaunchBookmark.user_id == user_id,
            LaunchBookmark.launch_id == bookmark.launch_id,
        )
        .first()
    )

    if existing_bookmark:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Launch already bookmarked"
        )

    # Create new bookmark
    db_bookmark = LaunchBookmark(user_id=user_id, launch_id=bookmark.launch_id)
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


@router.get(
    "/",
    response_model=List[Bookmark],
    summary="Get user bookmarks",
    description="Retrieve all bookmarks for the current user",
    responses={
        200: {
            "description": "List of user's bookmarks",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "launch_id": "5eb87cd9ffd86e000604b32a",
                            "created_at": "2025-06-08T12:12:43",
                        }
                    ]
                }
            },
        }
    },
)
def get_bookmarks(
    user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    bookmarks = db.query(LaunchBookmark).filter(LaunchBookmark.user_id == user_id).all()
    return bookmarks


@router.delete(
    "/{launch_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete bookmark",
    description="Delete a specific bookmark by launch ID",
    responses={
        204: {"description": "Bookmark successfully deleted"},
        404: {
            "description": "Bookmark not found",
            "content": {
                "application/json": {"example": {"detail": "Bookmark not found"}}
            },
        },
    },
)
def delete_bookmark(
    launch_id: str,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    bookmark = (
        db.query(LaunchBookmark)
        .filter(
            LaunchBookmark.user_id == user_id, LaunchBookmark.launch_id == launch_id
        )
        .first()
    )

    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found"
        )

    db.delete(bookmark)
    db.commit()
    return None
