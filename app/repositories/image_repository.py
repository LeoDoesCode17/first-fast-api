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

def get_by_id(db: Session, id: int):
    image_instance = db.query(Image).filter(Image.id == id, Image.is_deleted == False).first()
    if not image_instance:
        return None
    return image_instance

def delete(db: Session, id: int):
    image_instance = db.query(Image).filter(Image.id == id, Image.is_deleted == False).first()
    if not image_instance:
        return None
    image_instance.is_deleted = True
    db.commit()
    db.refresh(image_instance)
    return image_instance