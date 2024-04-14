from pydantic import BaseModel


class UserSignIn(BaseModel):
    email: str
    hashed_password: str


class UserSignUp(BaseModel):
    email: str
    hashed_password: str
    username: str


class UserUpdate(BaseModel):
    email: str
    hashed_password: str
    username: str


class UserList(BaseModel):
    id: int
    email: str
    hashed_password: str
    username: str


class UserDetail(BaseModel):
    id: int
    email: str
    hashed_password: str
    username: str
