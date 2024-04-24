from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.user import GetUser, UserSignUp, UserUpdate
from app.services.auth_jwt import get_active_user
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserSignUp, status_code=status.HTTP_201_CREATED)
async def user_create(
    user: UserSignUp,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
) -> GetUser:
    return await user_service.user_create(user=user, session=session)


@router.get("/", response_model=list[GetUser])
async def users_list(
    limit: int,
    offset: int,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
) -> list[GetUser]:
    return await user_service.users_list(limit=limit, offset=offset, session=session)


@router.get("/{user_id}", response_model=GetUser)
async def user_get(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
) -> GetUser:
    return await user_service.user_get(id=user_id, session=session)


@router.patch("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def user_deactivate(
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
) -> None:
    return await user_service.user_deactivate(user=user, session=session)


@router.patch("/{user_id}", response_model=UserUpdate)
async def user_update(
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
):
    return await user_service.user_update(
        user=user, user_data=user_data, session=session
    )
