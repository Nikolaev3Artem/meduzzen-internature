import jwt
from fastapi.security import HTTPAuthorizationCredentials

from app.core.config import settings
from app.schemas.auth import Token


class JWTSecurity:
    def create_jwt_token(payload_data: Token) -> Token:
        token = jwt.encode(
            payload=payload_data,
            key=settings.jwt_security_key,
            algorithm=settings.jwt_algorithm,
        )
        return Token(token=token)

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
