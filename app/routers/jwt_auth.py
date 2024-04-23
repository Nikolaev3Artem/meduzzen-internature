from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.user import UserSignIn, UserSignUp
from app.services.auth_jwt import JwtService, get_active_user
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def user_register(
    user_data: UserSignUp,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
):
    await user_service.user_create(user=user_data, session=session)
    return await JwtService.create_token(user_data, session, user_service)


@router.post("/login")
async def user_login(
    user_data: UserSignIn,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
):
    return await JwtService.create_token(user_data, session, user_service)


@router.get("/me")
async def get_me(
    user: User = Depends(get_active_user),
):
    return user
