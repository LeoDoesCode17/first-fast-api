# app/routes/users.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_current_user
from app.schemas.user import User, UserInDB
from sqlalchemy.orm import Session
from app.repositories import user_repository
from app.database import get_db
from app.schemas.user import UserResponse, PasswordChange
from app.core.security import verify_password

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    return current_user

@router.get("/me/items")
async def read_users_items():
    return {"item": "Hello"}

@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    return user_repository.get(db)

@router.post("/change-password", response_model=UserResponse)
async def change_password(
    schema: PasswordChange,
    current_user: Annotated[UserInDB, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    # Verifiy old password
    if not verify_password(schema.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Old password is incorrect'
        )
    
    # Verify password confirmation
    if not schema.new_password == schema.confirm_password:
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password confirmation failed'
        )      
    
    # Prevent set the same password
    if schema.old_password == schema.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='New password must be different'
        )
    
    updated_password_user = user_repository.update_password(db, user=current_user, new_password=schema.new_password)

    return updated_password_user