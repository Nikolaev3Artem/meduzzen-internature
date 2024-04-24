from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserNotFound
from app.core.hashing import Hasher
from app.db.alchemy.models import User
from app.schemas.user import UserBase, UserSignUp, UserUpdate


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
    async def list_users(limit: int, offset: int, session: AsyncSession) -> list[User]:
        users_list = await session.execute(
            select(User).limit(limit).offset(offset * limit)
        )
        return users_list.scalars().all()

    @staticmethod
    async def get_user(id: UUID, session: AsyncSession) -> User:
        user_data = await session.get(User, id)
        if user_data is None:
            raise UserNotFound(identifier_=id)
        return user_data

    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession) -> User:
        user_data = await session.execute(select(User).where(User.email == email))
        user_data = user_data.scalar()
        if user_data is None:
            raise UserNotFound(identifier_=email)
        return user_data

    @staticmethod
    async def delete_user(id: UUID, session: AsyncSession) -> None:
        user_data = await session.get(User, id)
        if user_data is None:
            raise UserNotFound(identifier_=id)
        await session.delete(user_data)
        await session.commit()
        return None

    @staticmethod
    async def update_user(
        id: UUID, user: UserUpdate, session: AsyncSession
    ) -> UserBase:
        user_in_db = await session.get(User, id)
        if user_in_db is None:
            raise UserNotFound(identifier_=id)
        user = user.model_dump(exclude_unset=True)

        for key, value in user.items():
            setattr(user_in_db, key, value)

        await session.commit()
        return user_in_db
