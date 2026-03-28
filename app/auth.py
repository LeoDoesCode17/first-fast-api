# app/auth.py
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from app.repositories.user_repository import get_by_username
from app.config import SECRET_KEY, ALGORITHM, fake_users_db
from app.schemas.token import TokenData
from app.schemas.user import User, UserInDB
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import verify_password, DUMMY_HASH

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, username: str):
    user = get_by_username(db, username)
    if not user:
        return None
    return user

def authenticate_user(db: Session, username: str, password: str) -> UserInDB | None:
    user = get_user(db, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Decode the JWT, look up the user, and raise 401 on any failure."""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if not user:
        raise credential_exception
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inactive user",
        )
    return user