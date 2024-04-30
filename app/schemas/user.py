from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserSignUp(UserBase):
    password: str


class UserUpdate(BaseModel):
    password: str | None = None
    username: str | None = None


class GetUser(UserBase):
    id: UUID


class UserDetail(GetUser):
    pass
