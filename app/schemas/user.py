from pydantic import BaseModel


class UserCreate(BaseModel):
    emais: str
    password: str
