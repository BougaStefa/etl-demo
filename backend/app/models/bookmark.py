from pydantic import BaseModel
from datetime import datetime
from .launch import Launch

class BookmarkBase(BaseModel):
    launch_id: str

class BookmarkCreate(BookmarkBase):
    pass

class Bookmark(BookmarkBase):
    id: int
    user_id: int
    created_at: datetime
    launch_id: str

    class Config:
        from_attributes = True
