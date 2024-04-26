from uuid import UUID

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: str


class CompanyCreate(CompanyBase):
    ...


class CompanyGet(CompanyBase):
    id: UUID


class CompanyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    visible: bool | None = None


class InvitationBase(BaseModel):
    user_id: UUID


class CreateInvitation(InvitationBase):
    ...


class GetInvitation(InvitationBase):
    id: UUID


class JoinRequestsBase(BaseModel):
    user_id: UUID


class GetJoinRequest(JoinRequestsBase):
    id: UUID
