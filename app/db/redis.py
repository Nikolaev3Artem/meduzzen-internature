import redis.asyncio as redis
from core.config import settings


async def redis_instanse():
    r = redis.Redis(
        host=settings.redis_host, port=settings.redis_port, db=settings.redis_databases
    )
    return r
