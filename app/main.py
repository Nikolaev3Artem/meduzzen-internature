import uvicorn
from fastapi import FastAPI
from routers.healthcheck import router as health_check_router
from core.config import settings

app = FastAPI()

app.include_router(health_check_router)

if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.api_host, port=settings.api_port, log_level="info", reload=settings.debug)