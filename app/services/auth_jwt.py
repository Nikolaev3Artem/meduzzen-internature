from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import Hasher
from app.core.security import create_jwt_token, get_user_by_token
from app.schemas.user import UserSignIn
from app.services.user import UserService


class JwtService:
    async def user_login(
        user_data: UserSignIn, session: AsyncSession, user_service: UserService
    ):
        db_user = await user_service.user_get_by_email(
            email=user_data.email, session=session
        )
        print(db_user)
        if Hasher.verify_password(
            plain_password=user_data.password, hashed_password=db_user.password
        ):
            payload_data = {"email": user_data.email}
            return create_jwt_token(payload_data=payload_data)

    async def me(token: str, session: AsyncSession, user_service: UserService):
        return await get_user_by_token(
            token=token, session=session, user_service=user_service
        )
