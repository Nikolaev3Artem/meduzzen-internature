from datetime import timedelta

import redis.asyncio as redis

from app.core.config import settings


class RedisService:
    def __init__(self):
        self._redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_databases,
        )

    async def set_cache(self, key: str, value: dict) -> None:
        await self._redis.set(key, value, ttl=timedelta(hours=48))
        await self._redis.expire(key, time=timedelta(hours=48))

    async def get_cache(self, key: str) -> dict:
        return await self._redis.get(key)
