import jwt
from fastapi.security import HTTPAuthorizationCredentials

from app.core.config import settings


class JWTSecurity:
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
            algorithms=["RS256"],
            audience=settings.auth0_audience,
            issuer=settings.auth0_issuer,
        )
        return payload
