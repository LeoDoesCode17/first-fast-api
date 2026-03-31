# app/schemas/tech.py
from pydantic import BaseModel

class TechCreate(BaseModel):
    name: str

class TechResponse(BaseModel):
    id: int
    name: str
    slug: str
    is_deleted: bool

class TechUpdate(TechCreate):
    pass
