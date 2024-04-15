from pydantic import BaseModel, EmailStr
from sqlalchemy.dialects.postgresql import UUID


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserSignUp(UserBase):
    password: str


class UserUpdate(BaseModel):
    password: str | None
    username: str | None


class GetUser(UserBase):
    id: UUID


class UserDetail(GetUser):
    pass
