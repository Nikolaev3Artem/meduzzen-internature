from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.user import UserSignIn
from app.services.auth_jwt import JwtService
from app.services.user import UserService

router = APIRouter(tags=["auth"])


@router.post("/login")
async def user_login(
    user_data: UserSignIn,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
):
    return await JwtService.user_login(user_data, session, user_service)


@router.get("/me")
async def get_me(
    user: User = Depends(JwtService.get_current_user),
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
):
    return user
