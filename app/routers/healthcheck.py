import redis.exceptions as redis_error
from db.postgress import get_session
from db.redis import Redis
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/redis")
async def redis_healthcheck() -> dict:
    try:
        redis = Redis()
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
    try:
        await session.execute(select(1))
        return {"status_code": 200, "detail": "ok", "result": "postgress working"}
    except Exception as e:
        return {"status_code": 500, "detail": e, "result": "postgress error"}


@router.get("/")
async def healthcheck() -> dict:
    return {"status_code": 200, "detail": "ok", "result": "working"}
