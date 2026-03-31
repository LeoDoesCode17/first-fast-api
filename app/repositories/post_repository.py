# app/repositories/post_repository.py
from sqlalchemy.orm import Session
from app.tables import Post
from app.schemas.post import PostCreate, PostUpdate
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

def update(db: Session, id: int, data: PostUpdate):
    post_instance = db.query(Post).filter(Post.id == id, Post.is_deleted == False).first()

    # if post with id doesn't exists
    if not post_instance:
        return None
    
    # update every key and val of post_instance 
    for key, val in data.model_dump().items():
        setattr(post_instance, key, val)

    db.commit()
    db.refresh(post_instance)
    return post_instance

def delete(db: Session, id: int):
    post_instance = db.query(Post).filter(Post.id == id, Post.is_deleted == False).first()
    if not post_instance:
        return None
    post_instance.is_deleted = True
    post_instance.is_published = False
    db.commit()
    db.refresh(post_instance)
    return post_instance

def publish(db: Session, id: int):
    post_instance = db.query(Post).filter(Post.id == id, Post.is_deleted == False, Post.is_published == False).first()
    if not post_instance:
        return None
    post_instance.is_published = True
    db.commit()
    db.refresh(post_instance)
    return post_instance
    