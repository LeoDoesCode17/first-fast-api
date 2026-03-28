# /app/repositories/user_repositories.py
from sqlalchemy.orm import Session
from app.tables import User
from app.core.security import get_password_hash

def get(db: Session):
    return db.query(User).filter(User.disabled == False).all()
def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.disabled == False).filter(User.username == username).first()
def update_password(db: Session, user: User, new_password: str):
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)
    return user