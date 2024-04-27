from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CompanyNotFound, InvitationNotFound
from app.db.alchemy.models import Company, CompanyRequests, RequestStatus
from app.db.postgress import get_session
from app.schemas.company import CompanyGet, GetInvitation
from app.schemas.user import GetJoinRequest


class CompanyRequestsRepos:
    def __init__(self):
        self._session = get_session()

    @staticmethod
    async def company_create_invitation(self, company_id: UUID, user_id: UUID) -> None:
        company_data = await self._session.get(Company, company_id)
        if not company_data or not company_data.visible:
            raise CompanyNotFound(identifier_=company_id)

        company_request = CompanyRequests(
            company_id=company_id,
            user_id=user_id,
            status=RequestStatus.INVITATION,
        )
        self._session.add(company_request)
        await self._session.commit()
        await self._session.refresh(company_request)
        return company_request

    @staticmethod
    async def company_delete_invitation(
        session: AsyncSession, invitation_id: UUID
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)

        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)

        if invitation.status != RequestStatus.MEMBER:
            await session.delete(invitation)
            await session.commit()

    @staticmethod
    async def invitations_list_company(
        company_id: UUID, session: AsyncSession
    ) -> list[CompanyGet]:
        invitations_list = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.INVITATION,
            )
        )
        return invitations_list.scalars().all()

    @staticmethod
    async def company_get_members(
        company_id: UUID, session: AsyncSession
    ) -> list[GetInvitation]:
        members_list = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.MEMBER,
            )
        )
        return members_list.scalars().all()

    @staticmethod
    async def company_kick_member(
        company_id: UUID, session: AsyncSession, user_id: UUID
    ) -> None:
        member = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.user_id == user_id,
                CompanyRequests.status == RequestStatus.MEMBER,
            )
        )
        await session.delete(member.scalar())
        await session.commit()

    @staticmethod
    async def company_join_requests_list(
        company_id: UUID, session: AsyncSession
    ) -> list[GetJoinRequest]:
        join_requests_list = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.JOIN_REQUEST,
            )
        )
        return join_requests_list.scalars().all()

    @staticmethod
    async def company_accept_join_request(
        session: AsyncSession, invitation_id: UUID
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)
        invitation.status = RequestStatus.MEMBER
        await session.commit()

    @staticmethod
    async def company_reject_join_request(
        session: AsyncSession, invitation_id: UUID
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(invitation)
        await session.commit()
