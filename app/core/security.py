import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.services.user import UserService


def create_jwt_token(payload_data: dict):
    return jwt.encode(
        payload=payload_data, key=settings.jwt_security_key, algorithm="HS256"
    )


async def get_user_by_token(
    token: str, user_service: UserService, session: AsyncSession
):
    user_email = jwt.decode(
        token,
        key=settings.jwt_security_key,
        algorithms=[
            "HS256",
        ],
    )
    print(user_email)
    return await user_service.user_get_by_email(
        email=user_email["email"], session=session
    )
