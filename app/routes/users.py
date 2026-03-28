from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.schemas.user import User
from sqlalchemy.orm import Session
from app.repositories import user_repository
from app.database import get_db
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    return current_user

@router.get("/me/items")
async def read_users_items(current_user: Annotated[User, Depends(get_current_user)]):
    return {"item": "Hello"}

@router.get("/", response_model=list[UserResponse])
async def get_all_users(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return user_repository.get(db)