# app/routes/techs.py
from app.database import get_db
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.schemas.tech import TechResponse, TechCreate
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