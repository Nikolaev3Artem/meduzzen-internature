from uuid import UUID

import redis.asyncio as redis
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.db.redis import RedisService
from app.schemas.quiz_results import QuizResultsCreate, QuizResultsGet
from app.services.auth_jwt import get_active_user
from app.services.quiz_results import QuizResultsService

quiz_results_router = APIRouter(
    prefix="/user/{user_id}/quiz_results", tags=["Quiz Results"]
)


@quiz_results_router.post(
    "/quiz/{quiz_id}/submit",
    response_model=QuizResultsGet,
    status_code=status.HTTP_200_OK,
)
async def submit_quiz_results(
    quiz_results: QuizResultsCreate,
    quiz_id: UUID,
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    quiz_results_service: QuizResultsService = Depends(QuizResultsService),
    user: User = Depends(get_active_user),
    redis_service: redis = Depends(RedisService),
) -> QuizResultsGet:
    return await quiz_results_service.quiz_submit(
        quiz_results=quiz_results,
        session=session,
        user=user,
        quiz_id=quiz_id,
        user_id=user_id,
        redis_service=redis_service,
    )


@quiz_results_router.get(
    "/{company_id}/avg_member_score", status_code=status.HTTP_200_OK
)
async def get_avg_member_score(
    company_id: UUID,
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    quiz_results_service: QuizResultsService = Depends(QuizResultsService),
    user: User = Depends(get_active_user),
) -> float:
    return await quiz_results_service.avg_company_member_score(
        session=session, user=user, company_id=company_id, user_id=user_id
    )


@quiz_results_router.get("/avg_user_score", status_code=status.HTTP_200_OK)
async def get_avg_user_score(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    quiz_results_service: QuizResultsService = Depends(QuizResultsService),
    user: User = Depends(get_active_user),
) -> float:
    return await quiz_results_service.avg_user_score(
        user_id=user_id, session=session, user=user
    )
