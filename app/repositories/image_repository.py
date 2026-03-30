# /app/repositories/image_repositories.py
from sqlalchemy.orm import Session
from app.tables import Image
from app.schemas.image import ImageCreate

def get(db: Session):
    return db.query(Image).filter(Image.is_deleted == False).all()

def create(db: Session, data: ImageCreate):
    image_instance = Image(**data.model_dump())
    db.add(image_instance)
    db.commit()
    db.refresh(image_instance)
    return image_instance