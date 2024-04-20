from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgress import get_session
from app.schemas.user import UserSignUp, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def user_create(user: UserSignUp, session: AsyncSession = Depends(get_session)):
    return await UserService.user_create(user, session)


@router.get("/")
async def users_list(
    limit: int, offset: int, session: AsyncSession = Depends(get_session)
):
    return await UserService.users_list(limit=limit, offset=offset, session=session)


@router.get("/{user_id}")
async def user_get(user_id: UUID, session: AsyncSession = Depends(get_session)):
    return await UserService.user_get(id=user_id, session=session)


@router.delete("/{user_id}")
async def user_delete(user_id: UUID, session: AsyncSession = Depends(get_session)):
    await UserService.user_delete(id=user_id, session=session)
    return status.HTTP_204_NO_CONTENT


@router.patch("/{user_id}")
async def user_update(
    user_id: UUID, user: UserUpdate, session: AsyncSession = Depends(get_session)
):
    return await UserService.user_update(id=user_id, user=user, session=session)
