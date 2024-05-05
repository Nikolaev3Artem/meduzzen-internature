import redis.exceptions as redis_error
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgress import get_session
from app.db.redis import RedisService

router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get("/redis")
async def redis_healthcheck() -> dict:
    try:
        redis = RedisService()
        await redis._redis.ping()
        return {"status_code": 200, "detail": "ok", "result": "redis working"}
    except redis_error.ConnectionError:
        return {
            "status_code": 500,
            "detail": "None",
            "result": "Connecting to redis was not successfull",
        }


@router.get("/postgress")
async def postgress_healthcheck(session: AsyncSession = Depends(get_session)) -> dict:
    await session.execute(select(1))
    return {"status_code": 200, "detail": "ok", "result": "postgress working"}


@router.get("/")
async def healthcheck() -> dict:
    return {"status_code": 200, "detail": "ok", "result": "working"}
