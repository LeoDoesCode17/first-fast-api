# app/routes/posts.py
from app.database import get_db
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.schemas.post import PostResponse, PostCreate, PostUpdate
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.repositories import post_repository

router = APIRouter(
    prefix='/posts',
    tags=['posts']
)

@router.get('/', response_model=list[PostResponse])
async def read_all_posts(db: Session = Depends(get_db)):
    return post_repository.get(db);

@router.post('/', response_model=PostResponse)
async def create_new_post(
    data: PostCreate, 
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db), 
):
    created_post = post_repository.create(db=db, data=data)
    if not created_post:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Slug already exists')
    return created_post

@router.patch('/{id}', response_model=PostResponse)
async def update_post(
    id: int,
    data: PostUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
): 
    updated_post = post_repository.update(db=db, id=id, data=data)
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post doesn't exist or slug already exists")
    return updated_post

@router.delete('/{id}', response_model=PostResponse)
async def delete_post(
    id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    deleted_post = post_repository.delete(db=db, id=id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found or already deleted'
        )
    return deleted_post
