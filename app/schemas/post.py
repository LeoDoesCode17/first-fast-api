# app/schemas/post.py
from pydantic import BaseModel
from datetime import datetime

class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    summary: str
    content: str
    is_deleted: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime

class PostCreate(BaseModel):
    title: str
    summary: str
    content: str

class PostUpdate(BaseModel):
    summary: str | None = None
    content: str | None = None
