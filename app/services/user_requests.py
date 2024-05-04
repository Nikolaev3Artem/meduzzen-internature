from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import RequestStatus
from app.core.exceptions import UserNotAllowed
from app.core.permissions import RoleChecker
from app.db.alchemy.models import User
from app.db.alchemy.repos.company import CompanyRepos
from app.db.alchemy.repos.user_requests import UserRequestsRepos
from app.schemas.user import GetUser
from app.schemas.user_requests import GetJoinRequest


class UserRequestsService:
    def __init__(self):
        self._repo = UserRequestsRepos()
        self._company_repo = CompanyRepos()

    async def user_invitation_list(
        self, session: AsyncSession, user: User, user_id: UUID
    ) -> list[GetUser]:
        RoleChecker.check_owner(allowed_user_id=user_id, user=user)
        return await self._repo.invitation_list_user(user_id=user_id, session=session)

    async def user_accept_invitation(
        self, invitation_id: UUID, session: AsyncSession, user: User
    ) -> None:
        invitation = await self._repo.get_invitation_user(
            invitation_id=invitation_id, session=session
        )

        if invitation.status == RequestStatus.MEMBER.value:
            raise UserNotAllowed(identifier_=user.id)

        RoleChecker.check_owner(allowed_user_id=invitation.user_id, user=user)
        return await self._repo.accept_invitation_user(
            invitation_id=invitation_id, session=session
        )

    async def user_reject_invitation(
        self, invitation_id: UUID, session: AsyncSession, user: User
    ) -> None:
        invitation = await self._repo.get_invitation_user(
            invitation_id=invitation_id, session=session
        )

        RoleChecker.check_owner(allowed_user_id=invitation.user_id, user=user)
        return await self._repo.reject_invitation_user(
            invitation_id=invitation_id, session=session
        )

    async def user_create_join_request(
        self,
        company_id: UUID,
        user: User,
        session: AsyncSession,
    ) -> GetJoinRequest:
        RoleChecker.check_owner(allowed_user_id=user.id, user=user)
        return await self._repo.user_create_join_request(
            user_id=user.id, session=session, company_id=company_id
        )

    async def user_list_join_request(
        self, user_id: UUID, user: User, session: AsyncSession
    ) -> list[GetJoinRequest]:
        RoleChecker.check_owner(allowed_user_id=user_id, user=user)
        return await self._repo.user_list_join_request(user_id=user_id, session=session)

    async def user_cancel_join_request(
        self, invitation_id: UUID, user: User, session: AsyncSession
    ) -> None:
        join_request = await self._repo.get_invitation_user(
            invitation_id=invitation_id, session=session
        )
        RoleChecker.check_owner(allowed_user_id=join_request.user_id, user=user)
        return await self._repo.user_cancel_join_request(
            invitation_id=invitation_id, session=session
        )

    async def user_company_leave(
        self, company_id: UUID, user: User, session: AsyncSession
    ) -> None:
        invitation = await self._repo.get_member_by_company(
            company_id=company_id, session=session
        )

        RoleChecker.check_owner(allowed_user_id=invitation.user_id, user=user)
        return await self._repo.user_company_leave(
            invitation_id=invitation.id, session=session
        )
