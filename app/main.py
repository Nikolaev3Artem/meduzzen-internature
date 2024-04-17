import uvicorn
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.healthcheck import router as health_check_router
from routers.user import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check_router, prefix="/healthcheck", tags=["Healthcheck"])
app.include_router(user_router, prefix="/user", tags=["User"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level="info",
        reload=settings.debug,
    )
