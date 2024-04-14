from pydantic import BaseModel


class UserSignIn(BaseModel):
    email: str
    password: str


class UserSignUp(BaseModel):
    email: str
    password: str
    username: str


class UserUpdate(BaseModel):
    password: str
    username: str


class UserList(BaseModel):
    email: str
    username: str


class UserDetail(BaseModel):
    email: str
    password: str
    username: str
