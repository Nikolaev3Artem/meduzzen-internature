from uuid import UUID

from db.postgress import get_session
from db.repos.user import create_user, delete_user, get_user, list_users, update_user
from fastapi import APIRouter, Depends
from schemas.user import GetUser, UserSignUp, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/user")


@router.post("/create/", response_model=GetUser)
async def user_create(user: UserSignUp, session: AsyncSession = Depends(get_session)):
    return await create_user(user=user, session=session)


@router.get("/")
async def users_list(session: AsyncSession = Depends(get_session)):
    return await list_users(session=session)


@router.get("/retrieve/")
async def user_get(id: UUID, session: AsyncSession = Depends(get_session)):
    return await get_user(id=id, session=session)


@router.delete("/delete/")
async def user_delete(id: UUID, session: AsyncSession = Depends(get_session)):
    user_status = await delete_user(id=id, session=session)

    if user_status:
        return {"status_code": 200, "detail": "ok", "result": "User deleted!"}

    return {"status_code": 500, "detail": "None", "result": "Undefined error"}


@router.patch("/update/")
async def user_update(
    id: UUID, user: UserUpdate, session: AsyncSession = Depends(get_session)
):
    return await update_user(id=id, session=session)
