import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.common import ObjNotFoundException
from app.core.config import settings
from app.routers.healthcheck import router as health_check_router
from app.routers.user import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ObjNotFoundException)
async def unicorn_exception_handler(request: Request, exc: ObjNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


app.include_router(health_check_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level="info",
        reload=settings.debug,
    )
