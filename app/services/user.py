from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import Hasher
from app.db.alchemy.repos.user import UserRepos
from app.schemas.user import UserSignUp, UserUpdate


class UserService:
    def __init__(self):
        self._repo = UserRepos

    async def user_create(self, user: UserSignUp, session: AsyncSession):
        return await self._repo.create_user(user=user, session=session)

    async def users_list(self, limit: int, offset: int, session: AsyncSession):
        return await self._repo.list_users(limit=limit, offset=offset, session=session)

    async def user_get(self, id: UUID, session: AsyncSession):
        return await self._repo.get_user(id=id, session=session)

    async def user_delete(self, id: UUID, session: AsyncSession):
        return await self._repo.delete_user(id=id, session=session)

    async def user_update(self, id: UUID, user: UserUpdate, session: AsyncSession):
        if user.password:
            user.password = Hasher.get_password_hash(user.password)

        return await self._repo.update_user(id=id, user=user, session=session)
