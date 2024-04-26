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


class InvitationBase(BaseModel):
    company_id: UUID


class GetInvitation(InvitationBase):
    id: UUID


class JoinRequestsBase(BaseModel):
    company_id: UUID


class CreateJoinRequest(JoinRequestsBase):
    ...


class GetJoinRequest(JoinRequestsBase):
    id: UUID
