from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotAllowed
from app.core.hashing import Hasher
from app.core.permissions import RoleChecker
from app.db.alchemy.models import RequestStatus, User
from app.db.alchemy.repos.user import UserRepos
from app.schemas.user import (
    CreateJoinRequest,
    GetInvitation,
    GetJoinRequest,
    GetUser,
    UserSignUp,
    UserUpdate,
)


class UserService:
    def __init__(self):
        self._repo = UserRepos()

    async def user_create(self, user: UserSignUp, session: AsyncSession) -> UserSignUp:
        return await self._repo.create_user(user=user, session=session)

    async def users_list(
        self, limit: int, offset: int, session: AsyncSession
    ) -> list[GetUser]:
        return await self._repo.list_users(limit=limit, offset=offset, session=session)

    async def user_get(self, id: UUID, session: AsyncSession) -> GetUser:
        return await self._repo.get_user(id=id, session=session)

    async def user_get_by_email(self, email: str, session: AsyncSession) -> GetUser:
        return await self._repo.get_user_by_email(email=email, session=session)

    async def user_deactivate(
        self, user_id: UUID, session: AsyncSession, user: User
    ) -> None:
        RoleChecker.check_permission(allowed_user_id=user_id, user=user)

        return await self._repo.deactivate_user(user_id=user_id, session=session)

    async def user_update(
        self, user_id: UUID, user_data: UserUpdate, session: AsyncSession, user: User
    ) -> GetUser:
        if user_data.password:
            user_data.password = Hasher.get_password_hash(user_data.password)

        RoleChecker.check_permission(allowed_user_id=user_id, user=user)

        return await self._repo.update_user(
            user_id=user_id, user_data=user_data, session=session
        )

    async def user_invitation_get(
        self, invitation_id: UUID, session: AsyncSession
    ) -> GetInvitation:
        return await self._repo.get_invitation_user(
            invitation_id=invitation_id, session=session
        )

    async def user_invitation_list(
        self, user_id: UUID, session: AsyncSession, user: User
    ) -> list[GetInvitation]:
        RoleChecker.check_permission(allowed_user_id=user_id, user=user)
        return await self._repo.invitation_list_user(user_id=user_id, session=session)

    async def user_accept_invitation(
        self, invitation_id: UUID, session: AsyncSession, user: User
    ) -> None:
        invitation = await UserService.user_invitation_get(
            self, invitation_id=invitation_id, session=session
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
        invitation = await UserService.user_invitation_get(
            self, invitation_id=invitation_id, session=session
        )
        RoleChecker.check_permission(allowed_user_id=invitation.user_id, user=user)
        return await self._repo.reject_invitation_user(
            invitation_id=invitation_id, session=session
        )

    async def user_create_join_request(
        self,
        user_id: UUID,
        create_join_request: CreateJoinRequest,
        user: User,
        session: AsyncSession,
    ) -> GetJoinRequest:
        RoleChecker.check_permission(allowed_user_id=user_id, user=user)
        return await self._repo.user_create_join_request(
            user_id=user_id, session=session, create_join_request=create_join_request
        )

    async def user_list_join_request(
        self, user_id: UUID, user: User, session: AsyncSession
    ) -> list[GetJoinRequest]:
        RoleChecker.check_permission(allowed_user_id=user_id, user=user)
        return await self._repo.user_list_join_request(user_id=user_id, session=session)

    async def user_cancel_join_request(
        self, invitation_id: UUID, user: User, session: AsyncSession
    ) -> None:
        join_request = await UserService.user_invitation_get(
            self, invitation_id=invitation_id, session=session
        )
        RoleChecker.check_permission(allowed_user_id=join_request.user_id, user=user)
        return await self._repo.user_cancel_join_request(
            invitation_id=invitation_id, session=session
        )

    async def user_company_leave(
        self, invitation_id: UUID, user: User, session: AsyncSession
    ) -> None:
        company_request = await UserService.user_invitation_get(
            self, invitation_id=invitation_id, session=session
        )
        RoleChecker.check_permission(allowed_user_id=company_request.user_id, user=user)
        return await self._repo.user_company_leave(
            invitation_id=invitation_id, session=session
        )
