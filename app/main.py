from fastapi import FastAPI
from routers.healthcheck import router as health_check_router

app = FastAPI()

app.include_router(health_check_router)