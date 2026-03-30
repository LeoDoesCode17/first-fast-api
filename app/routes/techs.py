# app/routes/techs.py
from app.database import get_db
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.schemas.tech import TechResponse, TechCreate, TechUpdate
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session
from app.repositories import tech_repository

router = APIRouter(
    prefix='/techs',
    tags=['techs'],
)

@router.get('/', response_model=list[TechResponse])
async def read_all_techs(db: Session = Depends(get_db)):
    return tech_repository.get(db)

@router.post('/', response_model=TechResponse)
async def create_tech(
    tech: TechCreate, 
    current_user: Annotated[UserResponse, Depends(get_current_user)], 
    db: Session = Depends(get_db)
):
    return tech_repository.create(db, data=tech)

@router.delete('/{id}', response_model=TechResponse)
async def soft_delete_tech(
    id: int,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return tech_repository.delete(db, id)

@router.patch('/{id}', response_model=TechResponse)
async def update_tech(
    id: int,
    data: TechUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    updated_tech = tech_repository.update(db=db, id=id, data=data)
    if not updated_tech:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tech not found or already deleted")
    return updated_tech