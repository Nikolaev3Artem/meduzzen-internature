import jwt
from fastapi.security import HTTPAuthorizationCredentials

from app.core.config import settings


def create_jwt_token(payload_data: dict):
    return jwt.encode(
        payload=payload_data, key=settings.jwt_security_key, algorithm="HS256"
    )


async def get_user_by_token(token: HTTPAuthorizationCredentials):
    return jwt.decode(
        token.credentials,
        key=settings.jwt_security_key,
        algorithms=[
            "HS256",
        ],
    )
