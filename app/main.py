import uvicorn
from fastapi import FastAPI
from app.routers.healthcheck import router as health_check_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check_router)
if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.api_host, port=settings.api_port, log_level="info", reload=settings.debug)