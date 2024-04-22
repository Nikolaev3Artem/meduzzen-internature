from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import Hasher
from app.core.security import create_jwt_token, get_user_by_token
from app.db.postgress import get_session
from app.schemas.user import UserSignIn
from app.services.user import UserService

security = HTTPBearer()


class JwtService:
    async def user_login(
        user_data: UserSignIn,
        session: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(UserService),
    ):
        db_user = await user_service.user_get_by_email(
            email=user_data.email, session=session
        )
        if Hasher.verify_password(
            plain_password=user_data.password, hashed_password=db_user.password
        ):
            payload_data = {"email": user_data.email}
            return create_jwt_token(payload_data=payload_data)

    async def get_current_user(
        token: HTTPAuthorizationCredentials = Security(security),
        session: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(UserService),
    ):
        user_email = await get_user_by_token(token=token)
        return await user_service.user_get_by_email(
            email=user_email["email"], session=session
        )
