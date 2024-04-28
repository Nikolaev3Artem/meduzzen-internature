from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import RequestStatus
from app.core.exceptions import (
    CompanyNotFound,
    InvitationAlreadyExists,
    InvitationNotFound,
    MemberNotFound,
)
from app.db.alchemy.models import Company, CompanyRequests, User
from app.schemas.company import GetInvitation
from app.schemas.user import GetJoinRequest, GetUser


class CompanyRequestsRepos:
    @staticmethod
    async def company_create_invitation(
        company_id: UUID, user_id: UUID, session: AsyncSession
    ) -> None:
        company_data = await session.get(Company, company_id)
        if not company_data or not company_data.visible:
            raise CompanyNotFound(identifier_=company_id)

        company_request = CompanyRequests(
            company_id=company_id,
            user_id=user_id,
            status=RequestStatus.INVITATION,
        )
        session.add(company_request)
        await session.commit()
        await session.refresh(company_request)
        return company_request

    @staticmethod
    async def company_delete_invitation(
        session: AsyncSession, invitation_id: UUID
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)

        if not invitation or invitation.status == RequestStatus.MEMBER:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(invitation)
        await session.commit()

    @staticmethod
    async def invitations_list_company(
        company_id: UUID, session: AsyncSession
    ) -> list[GetUser]:
        invitations_list = await session.execute(
            select(User)
            .join(CompanyRequests)
            .where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.INVITATION,
            )
        )
        return invitations_list.scalars().all()

    @staticmethod
    async def company_get_members(
        company_id: UUID, session: AsyncSession
    ) -> list[GetUser]:
        members_list = await session.execute(
            select(User)
            .join(CompanyRequests)
            .where(
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
        if not member:
            raise MemberNotFound(identifier_=user_id)

        await session.delete(member.scalar())
        await session.commit()

    @staticmethod
    async def company_join_requests_list(
        company_id: UUID, session: AsyncSession
    ) -> list[GetUser]:
        join_requests_list = await session.execute(
            select(User)
            .join(CompanyRequests)
            .where(
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

    @staticmethod
    async def get_invitation_user(
        invitation_id: UUID, session: AsyncSession
    ) -> GetInvitation:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)
        return invitation

    @staticmethod
    async def get_invitation_by_company(
        company_id: UUID, session: AsyncSession
    ) -> GetInvitation:
        invitation = await session.execute(
            select(CompanyRequests).where(CompanyRequests.company_id == company_id)
        )
        invitation = invitation.scalar()

        if not invitation:
            raise InvitationNotFound(identifier_=company_id)

        return invitation

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
    async def check_invitation_exists(
        company_id: UUID, user_id: UUID, session: AsyncSession
    ) -> None:
        invitation_exists = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.user_id == user_id,
            )
        )
        invitation_exists = invitation_exists.scalar()
        if invitation_exists:
            raise InvitationAlreadyExists(
                column_name_="company_id, user_id",
                input_data_=f"{invitation_exists.company_id}, {invitation_exists.user_id}",
            )
