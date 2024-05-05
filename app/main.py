import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import (
    IntegritiError,
    NotAllowed,
    NotAuthorized,
    ObjectNotFound,
)
from app.routers.company import router as company_router
from app.routers.company_requests import company_requests_router
from app.routers.healthcheck import router as health_check_router
from app.routers.jwt_auth import router as auth_router
from app.routers.quiz import router as quiz_router
from app.routers.quiz_results import quiz_results_router
from app.routers.user import router as user_router
from app.routers.user_requests import user_requests_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ObjectNotFound)
async def not_found_exception_handler(request: Request, exc: ObjectNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.msg},
    )


@app.exception_handler(NotAllowed)
async def not_allowed_exception_handler(request: Request, exc: ObjectNotFound):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"message": exc.msg},
    )


@app.exception_handler(NotAuthorized)
async def unathorized_exception_handler(request: Request, exc: ObjectNotFound):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.msg},
    )


@app.exception_handler(IntegritiError)
async def integrity_error_exception_handler(request: Request, exc: ObjectNotFound):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.msg},
    )


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(company_router)
app.include_router(user_requests_router)
app.include_router(company_requests_router)
app.include_router(quiz_router)
app.include_router(quiz_results_router)
app.include_router(health_check_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level="info",
        reload=settings.debug,
    )
