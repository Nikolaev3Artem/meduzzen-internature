from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotAllowed
from app.core.permissions import RoleChecker
from app.db.alchemy.models import RequestStatus, User
from app.db.alchemy.repos.company import CompanyRepos
from app.db.alchemy.repos.company_requests import CompanyRequestsRepos
from app.schemas.company import GetInvitation
from app.schemas.user import GetJoinRequest, GetUser


class CompanyRequestsService:
    def __init__(self):
        self._repo = CompanyRequestsRepos()
        self._company_repo = CompanyRepos()

    async def company_create_invitation(
        self,
        company_id: UUID,
        user_id: UUID,
        user: User,
        session: AsyncSession,
    ) -> GetInvitation:
        await self._repo.check_invitation_exists(
            user_id=user_id, session=session, company_id=company_id
        )
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)

        return await self._repo.company_create_invitation(
            company_id=company_id, user_id=user_id, session=session
        )

    async def company_delete_invitation(
        self, company_id: UUID, invitation_id: UUID, user: User, session: AsyncSession
    ) -> GetInvitation:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )

        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)

        return await self._repo.company_delete_invitation(
            session=session, invitation_id=invitation_id
        )

    async def company_invitations_list(
        self, user: User, company_id: UUID, session: AsyncSession
    ) -> list[GetUser]:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.invitations_list_company(
            company_id=company_id, session=session
        )

    async def company_get_members(
        self, user: User, company_id: UUID, session: AsyncSession
    ) -> list[GetUser]:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_get_members(
            company_id=company_id, session=session
        )

    async def company_kick_member(
        self, user: User, user_id: UUID, company_id: UUID, session: AsyncSession
    ) -> list[GetInvitation]:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_kick_member(
            company_id=company_id, session=session, user_id=user_id
        )

    async def company_join_requests_list(
        self, user: User, company_id: UUID, session: AsyncSession
    ) -> list[GetUser]:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_join_requests_list(
            company_id=company_id, session=session
        )

    async def accept_join_request(
        self, user: User, company_id: UUID, invitation_id: UUID, session: AsyncSession
    ) -> None:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_accept_join_request(
            session=session, invitation_id=invitation_id
        )

    async def reject_join_request(
        self, user: User, company_id: UUID, invitation_id: UUID, session: AsyncSession
    ) -> None:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_reject_join_request(
            session=session, invitation_id=invitation_id
        )

    async def get_invitation_user(
        self, invitation_id: UUID, session: AsyncSession
    ) -> GetInvitation:
        return await self._repo.get_invitation_user(
            invitation_id=invitation_id, session=session
        )

    async def user_invitation_list(
        self, session: AsyncSession, user: User, user_id: UUID
    ) -> list[GetUser]:
        RoleChecker.check_permission(allowed_user_id=user_id, user=user)
        return await self._repo.invitation_list_user(user_id=user_id, session=session)

    async def user_accept_invitation(
        self, invitation_id: UUID, session: AsyncSession, user: User
    ) -> None:
        invitation = await self._repo.get_invitation_user(
            invitation_id=invitation_id, session=session
        )

        if invitation.status == RequestStatus.MEMBER:
            raise UserNotAllowed(identifier_=user.id)

        RoleChecker.check_permission(allowed_user_id=invitation.user_id, user=user)
        return await self._repo.accept_invitation_user(
            invitation_id=invitation_id, session=session
        )

    async def user_reject_invitation(
        self, invitation_id: UUID, session: AsyncSession, user: User
    ) -> None:
        invitation = await self._repo.get_invitation_user(
            invitation_id=invitation_id, session=session
        )

        RoleChecker.check_permission(allowed_user_id=invitation.user_id, user=user)
        return await self._repo.reject_invitation_user(
            invitation_id=invitation_id, session=session
        )

    async def user_create_join_request(
        self,
        company_id: UUID,
        user: User,
        session: AsyncSession,
    ) -> GetJoinRequest:
        await self._repo.check_invitation_exists(
            user_id=user.id, session=session, company_id=company_id
        )
        RoleChecker.check_permission(allowed_user_id=user.id, user=user)
        return await self._repo.user_create_join_request(
            user_id=user.id, session=session, company_id=company_id
        )

    async def user_list_join_request(
        self, user_id: UUID, user: User, session: AsyncSession
    ) -> list[GetJoinRequest]:
        RoleChecker.check_permission(allowed_user_id=user_id, user=user)
        return await self._repo.user_list_join_request(user_id=user_id, session=session)

    async def user_cancel_join_request(
        self, invitation_id: UUID, user: User, session: AsyncSession
    ) -> None:
        join_request = await self._repo.get_invitation_user(
            invitation_id=invitation_id, session=session
        )
        RoleChecker.check_permission(allowed_user_id=join_request.user_id, user=user)
        return await self._repo.user_cancel_join_request(
            invitation_id=invitation_id, session=session
        )

    async def user_company_leave(
        self, company_id: UUID, user: User, session: AsyncSession
    ) -> None:
        invitation = await self._repo.get_invitation_by_company(
            company_id=company_id, session=session
        )

        RoleChecker.check_permission(allowed_user_id=invitation.user_id, user=user)
        return await self._repo.user_company_leave(
            invitation_id=invitation.id, session=session
        )
