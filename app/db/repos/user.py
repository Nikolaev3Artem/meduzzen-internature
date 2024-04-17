from uuid import UUID

from core.hashing import Hasher
from db.alchemy.models import User
from schemas.user import UserSignUp, UserUpdate
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


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


async def list_users(session: AsyncSession) -> list[User]:
    users_list = await session.execute(select(User))
    result = [list(user) for user in users_list]
    return result


async def get_user(id: UUID, session: AsyncSession) -> User:
    user = await session.execute(select(User).where(User.id == id))
    return user.scalar()


async def delete_user(id: UUID, session: AsyncSession) -> bool:
    await session.execute(delete(User).where(User.id == id))
    await session.commit()
    return True


async def update_user(id: UUID, user: UserUpdate, session: AsyncSession) -> bool:
    await session.execute(update(User).where(User.id == id))
    await session.commit()
    return True
