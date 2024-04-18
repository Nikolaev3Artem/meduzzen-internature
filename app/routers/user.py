from uuid import UUID

from app.db.postgress import get_session
from fastapi import APIRouter, Depends
from app.schemas.user import GetUser, UserSignUp, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService

router = APIRouter()


@router.post("/create", response_model=GetUser)
async def user_create(user: UserSignUp, session: AsyncSession = Depends(get_session)):
    return await UserService.user_create(user, session)


@router.get("/")
async def users_list(session: AsyncSession = Depends(get_session)):
    return await UserService.users_list(session=session)


@router.get("/{user_id}/retrieve")
async def user_get(id: UUID, session: AsyncSession = Depends(get_session)):
    return await UserService.user_get(id=id, session=session)


@router.delete("/{user_id}/delete")
async def user_delete(id: UUID, session: AsyncSession = Depends(get_session)):
    user_status = await UserService.user_delete(id=id, session=session)

    if user_status:
        return {"status_code": 200, "detail": "ok", "result": "User deleted!"}

    return {"status_code": 500, "detail": "None", "result": "Undefined error"}


@router.patch("/{user_id}/update")
async def user_update(
    id: UUID, user: UserUpdate, session: AsyncSession = Depends(get_session)
):
    return await UserService.user_update(id=id, user=user, session=session)
