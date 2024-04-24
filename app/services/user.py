from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import Hasher
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

    async def user_deactivate(self, user: User, session: AsyncSession) -> None:
        return await self._repo.deactivate_user(user=user, session=session)

    async def user_update(
        self, user: User, user_data: UserUpdate, session: AsyncSession
    ) -> GetUser:
        if user.password:
            user.password = Hasher.get_password_hash(user.password)

        return await self._repo.update_user(
            user=user, user_data=user_data, session=session
        )
