from uuid import UUID

from pydantic import BaseModel


class JoinRequestsBase(BaseModel):
    company_id: UUID


class GetJoinRequest(JoinRequestsBase):
    id: UUID
