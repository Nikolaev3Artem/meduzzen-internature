import redis.asyncio as redis

from core.config import settings

r = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, db=settings.redis_databases
)
