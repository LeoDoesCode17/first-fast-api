# app/schemas/image.py
from pydantic import BaseModel

class ImageResponse(BaseModel):
    id: int
    name: str
    url: str
    alt_text: str
    is_deleted: bool

class ImageCreate(BaseModel):
    name: str
    url: str
    alt_text: str

class ImageUpdate(ImageCreate):
    pass