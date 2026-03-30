# app/routes/images.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_current_user
from app.repositories import image_repository
from app.database import get_db
from app.schemas.image import ImageResponse, ImageCreate
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/images',
    tags=['images'],
    dependencies=[Depends(get_current_user)]
)

@router.get('/')
async def read_all_images(db: Session = Depends(get_db)):
    images = image_repository.get(db)
    return images

@router.post('/', response_model=ImageResponse)
async def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    image = image_repository.create(db=db, data=image)
    return image
