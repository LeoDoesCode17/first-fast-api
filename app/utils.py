import jwt
from datetime import datetime, timedelta, timezone
from app.config import SECRET_KEY, ALGORITHM


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Encode user data into a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)