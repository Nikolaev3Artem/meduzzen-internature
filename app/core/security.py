import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import NotAuthorized
from app.core.hashing import Hasher
from app.db.postgress import get_session
from app.schemas.auth import Token
from app.schemas.user import UserSignIn
from app.services.user import UserService


class JWTSecurity:
    async def create_jwt_token(
        user_data: UserSignIn,
        session: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(UserService),
    ) -> Token:
        db_user = await user_service.user_get_by_email(
            email=user_data.email, session=session
        )
        if Hasher.verify_password(
            plain_password=user_data.password, hashed_password=db_user.password
        ):
            payload_data = {"email": user_data.email}
            token = jwt.encode(
                payload=payload_data,
                key=settings.jwt_security_key,
                algorithm=settings.jwt_algorithm,
            )
            return Token(token=token)
        raise NotAuthorized()

    async def get_user_by_token(token: HTTPAuthorizationCredentials):
        return jwt.decode(
            token.credentials,
            key=settings.jwt_security_key,
            algorithms=settings.jwt_algorithm,
        )


class Auth0Security:
    async def get_user_email(token: HTTPAuthorizationCredentials):
        JWKS_CLIENT = jwt.PyJWKClient(
            f"https://{settings.auth0_domain}/.well-known/jwks.json"
        )
        signing_data = JWKS_CLIENT.get_signing_key_from_jwt(token.credentials)
        signing_key = signing_data.key

        payload = jwt.decode(
            token.credentials,
            signing_key,
            algorithms=settings.auth0_algorithm,
            audience=settings.auth0_audience,
            issuer=settings.auth0_issuer,
        )
        return payload
