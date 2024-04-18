from uuid import UUID

from app.core.hashing import Hasher
from app.db.alchemy.models import User
from app.schemas.user import UserSignUp, UserUpdate, UserBase
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepos:
    @staticmethod
    async def create_user(user: UserSignUp, session: AsyncSession) -> User:
        user = User(
            email=user.email,
            password=Hasher.get_password_hash(user.password),
            username=user.username,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def list_users(session: AsyncSession) -> list[User]:
        users_list = await session.execute(select(User))
        result = [list(user) for user in users_list]
        return result

    @staticmethod
    async def get_user(id: UUID, session: AsyncSession) -> User:
        user = await session.execute(select(User).where(User.id == id))
        return user.scalar()

    @staticmethod
    async def delete_user(id: UUID, session: AsyncSession) -> bool:
        await session.execute(delete(User).where(User.id == id))
        await session.commit()
        return True

    @staticmethod
    async def update_user(
        id: UUID, user: UserUpdate, session: AsyncSession
    ) -> UserBase:
        get_user = await UserRepos.get_user(id, session)
        user_data = user.dict(exclude_unset=True)

        if "password" in user_data:
            user_data["password"] = Hasher.get_password_hash(user_data["password"])

        for key, value in user_data.items():
            setattr(get_user, key, value)

        await session.commit()
        return get_user
