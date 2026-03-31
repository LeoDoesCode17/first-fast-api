# /app/repositories/tech_repositories.py
from sqlalchemy.orm import Session
from app.tables import Tech
from app.schemas.tech import TechCreate, TechUpdate
from slugify import slugify

def get(db: Session):
    return db.query(Tech).filter(Tech.is_deleted == False).all()

def create(db: Session, data: TechCreate):
    tech_instance = Tech(**data.model_dump())
    if not tech_instance.slug:
        tech_instance.slug = slugify(tech_instance.name)
    db.add(tech_instance)
    db.commit()
    db.refresh(tech_instance)
    return tech_instance

def delete(db: Session, id: int):
    tech_instance = db.query(Tech).filter(Tech.id == id, Tech.is_deleted == False).first()
    if not tech_instance:
        return None
    tech_instance.is_deleted = True
    db.commit()
    db.refresh(tech_instance)
    return tech_instance

def update(db: Session, id: int, data: TechUpdate):
    tech_instance = db.query(Tech).filter(Tech.id == id, Tech.is_deleted == False).first()
    if not tech_instance:
        return None
    for key, val in data.model_dump().items():
        setattr(tech_instance, key, val)
    db.commit()
    db.refresh(tech_instance)
    return tech_instance
    
