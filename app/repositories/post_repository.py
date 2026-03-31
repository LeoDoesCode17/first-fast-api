# app/repositories/post_repository.py
from sqlalchemy.orm import Session
from app.tables import Post
from app.schemas.post import PostCreate, PostResponse
from slugify import slugify

def get(db: Session):
    return db.query(Post).filter(Post.is_deleted == False, Post.is_published == True).all()

def create(db: Session, data: PostCreate):
    # look for a post that has same slug
    post_instance = Post(**data.model_dump())
    post_instance.slug = slugify(post_instance.title)
    same_slug = db.query(Post).filter(Post.slug == post_instance.slug).first()
    if same_slug:
        return None
    db.add(post_instance)
    db.commit()
    db.refresh(post_instance)
    return post_instance