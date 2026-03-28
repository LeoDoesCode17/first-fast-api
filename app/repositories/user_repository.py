# /app/repositories/user_repositories.py
from sqlalchemy.orm import Session
from app.tables import User

def get(db: Session):
    return db.query(User).filter(User.disabled == False).all()
def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.disabled == False).filter(User.username == username).first()
