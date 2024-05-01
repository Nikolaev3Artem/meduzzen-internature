from uuid import UUID

from pydantic import BaseModel


class InvitationBase(BaseModel):
    user_id: UUID


class GetInvitation(InvitationBase):
    id: UUID
