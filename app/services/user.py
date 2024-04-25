from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import Hasher
from app.core.permissions import RoleChecker
from app.db.alchemy.models import User
from app.db.alchemy.repos.user import UserRepos
from app.schemas.user import GetUser, UserSignUp, UserUpdate


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
        if RoleChecker.check_permission(allowed_user_id=user_id, user=user):
            return await self._repo.deactivate_user(user_id=user_id, session=session)

    async def user_update(
        self, user_id: UUID, user_data: UserUpdate, session: AsyncSession, user: User
    ) -> GetUser:
        if user_data.password:
            user_data.password = Hasher.get_password_hash(user_data.password)
        if RoleChecker.check_permission(allowed_user_id=user_id, user=user):
            return await self._repo.update_user(
                user_id=user_id, user_data=user_data, session=session
            )
