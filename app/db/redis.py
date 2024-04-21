import redis.asyncio as redis
from app.core.config import settings


class Redis:
    def __init__(self):
        self._redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_databases,
        )
