# /app/repositories/tech_repositories.py
from sqlalchemy.orm import Session
from app.tables import Tech
from app.schemas.tech import TechCreate

def get(db: Session):
    return db.query(Tech).all()

def create(db: Session, data: TechCreate):
    tech_instance = Tech(**data.model_dump())
    db.add(tech_instance)
    db.commit()
    db.refresh(tech_instance)
    return tech_instance

def delete(db: Session, id: int):
    tech_instance = db.query(Tech).filter(Tech.id == id).first()
    if tech_instance:
        tech_instance.is_deleted = True
        db.commit()
        db.refresh(tech_instance)
    return tech_instance
