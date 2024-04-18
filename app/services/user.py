from app.db.alchemy.repos.user import UserRepos
from app.schemas.user import UserSignUp, UserUpdate
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    async def user_create(user: UserSignUp, session: AsyncSession):
        return await UserRepos.create_user(user=user, session=session)

    async def users_list(session: AsyncSession):
        return await UserRepos.list_users(session=session)

    async def user_get(id: UUID, session: AsyncSession):
        return await UserRepos.get_user(id=id, session=session)

    async def user_delete(id: UUID, session: AsyncSession):
        user_status = await UserRepos.delete_user(id=id, session=session)
        return user_status

    async def user_update(id: UUID, user: UserUpdate, session: AsyncSession):
        return await UserRepos.update_user(id=id, user=user, session=session)
