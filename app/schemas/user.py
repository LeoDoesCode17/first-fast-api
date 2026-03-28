from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserResponse(User):
    class config:
        from_attributes = True

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str


class UserInDB(User):
    hashed_password: str