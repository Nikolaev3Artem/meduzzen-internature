from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import Hasher
from app.db.alchemy.repos.user import UserRepos
from app.schemas.user import UserSignUp, UserUpdate


class UserService:
    async def user_create(user: UserSignUp, session: AsyncSession):
        return await UserRepos.create_user(user=user, session=session)

    async def users_list(limit: int, offset: int, session: AsyncSession):
        return await UserRepos.list_users(limit=limit, offset=offset, session=session)

    async def user_get(id: UUID, session: AsyncSession):
        return await UserRepos.get_user(id=id, session=session)

    async def user_delete(id: UUID, session: AsyncSession):
        return await UserRepos.delete_user(id=id, session=session)

    async def user_update(id: UUID, user: UserUpdate, session: AsyncSession):
        if user.password:
            user.password = Hasher.get_password_hash(user.password)

        return await UserRepos.update_user(id=id, user=user, session=session)
