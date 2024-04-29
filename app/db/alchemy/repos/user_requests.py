from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import RequestStatus
from app.core.exceptions import CompanyNotFound, InvitationNotFound
from app.db.alchemy.models import Company, CompanyRequests, User
from app.schemas.company import GetInvitation
from app.schemas.user import GetJoinRequest, GetUser


class UserRequestsRepos:
    @staticmethod
    async def invitation_list_user(
        user_id: UUID, session: AsyncSession
    ) -> list[GetUser]:
        invitations_list = await session.execute(
            select(User)
            .join(CompanyRequests)
            .where(
                CompanyRequests.user_id == user_id,
                CompanyRequests.status == RequestStatus.INVITATION,
            )
        )
        return invitations_list.scalars().all()

    @staticmethod
    async def accept_invitation_user(
        invitation_id: UUID, session: AsyncSession
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)
        invitation.status = RequestStatus.MEMBER
        await session.commit()

    @staticmethod
    async def reject_invitation_user(
        invitation_id: UUID, session: AsyncSession
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation or invitation.status == RequestStatus.MEMBER:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(invitation)
        await session.commit()

    @staticmethod
    async def user_create_join_request(
        user_id: UUID, session: AsyncSession, company_id: UUID
    ) -> GetJoinRequest:
        company_data = await session.get(Company, company_id)
        if not company_data or not company_data.visible:
            raise CompanyNotFound(identifier_=company_id)

        user_join_request = CompanyRequests(
            company_id=company_id,
            user_id=user_id,
            status=RequestStatus.JOIN_REQUEST,
        )
        session.add(user_join_request)
        await session.commit()
        await session.refresh(user_join_request)
        return user_join_request

    @staticmethod
    async def user_list_join_request(
        user_id: UUID, session: AsyncSession
    ) -> list[GetJoinRequest]:
        invitation_list = await session.execute(
            select(User)
            .join(CompanyRequests)
            .where(
                CompanyRequests.user_id == user_id,
                CompanyRequests.status == RequestStatus.JOIN_REQUEST,
            )
        )
        return invitation_list

    @staticmethod
    async def user_cancel_join_request(
        invitation_id: UUID, session: AsyncSession
    ) -> None:
        join_request = await session.get(CompanyRequests, invitation_id)
        if not join_request or join_request.status == RequestStatus.MEMBER:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(join_request)
        await session.commit()

    @staticmethod
    async def user_company_leave(invitation_id: UUID, session: AsyncSession) -> None:
        join_request = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.id == invitation_id,
                CompanyRequests.status == RequestStatus.MEMBER,
            )
        )
        join_request = join_request.scalar()
        if not join_request:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(join_request)
        await session.commit()

    @staticmethod
    async def get_invitation_user(
        invitation_id: UUID, session: AsyncSession
    ) -> GetInvitation:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)
        return invitation

    @staticmethod
    async def get_member_by_company(
        company_id: UUID, session: AsyncSession
    ) -> GetInvitation:
        invitation = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.MEMBER,
            )
        )
        invitation = invitation.scalar()

        if not invitation:
            raise InvitationNotFound(identifier_=company_id)

        return invitation
