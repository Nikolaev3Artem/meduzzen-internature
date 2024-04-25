from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import Auth0Security, JWTSecurity
from app.db.postgress import get_session
from app.schemas.auth import Token
from app.schemas.user import GetUser, UserSignIn
from app.services.user import UserService

security = HTTPBearer()


class JwtService:
    async def create_token(
        user_data: UserSignIn,
        session: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(UserService),
    ) -> Token:
        return await JWTSecurity.create_jwt_token(
            user_data=user_data, session=session, user_service=user_service
        )

    async def get_token_data(token: HTTPAuthorizationCredentials) -> str:
        return await JWTSecurity.get_user_by_token(token=token)


class Auth0Service:
    async def get_token_data(token: HTTPAuthorizationCredentials) -> str:
        return await Auth0Security.get_user_email(token)


async def get_active_user(
    token: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
) -> GetUser:
    try:
        user_email = await JwtService.get_token_data(token)
    except:
        user_email = await Auth0Service.get_token_data(token)

    return await user_service.user_get_by_email(
        email=user_email["email"], session=session
    )
