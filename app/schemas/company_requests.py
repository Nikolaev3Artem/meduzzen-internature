from uuid import UUID

from pydantic import BaseModel


class CompanyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    visible: bool | None = None


class InvitationBase(BaseModel):
    user_id: UUID


class GetInvitation(InvitationBase):
    id: UUID
