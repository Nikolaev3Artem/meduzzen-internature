from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.init_postgress import get_session
from db.init_redis import r

router = APIRouter()


@router.get("/")
async def healthcheck(session: AsyncSession = Depends(get_session)):
    await session.execute(select(1))
    await r.set("test", "redis connected")
    print(await r.get("test"))
    return {"status_code": 200, "detail": "ok", "result": "working"}
