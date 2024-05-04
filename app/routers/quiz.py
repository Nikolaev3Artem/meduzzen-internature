from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.quiz import QuizCreate, QuizGet, QuizUpdate
from app.services.auth_jwt import get_active_user
from app.services.quiz import QuizService

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.post(
    "/{company_id}/create_quiz",
    response_model=QuizGet,
    status_code=status.HTTP_201_CREATED,
)
async def quiz_create(
    quiz: QuizCreate,
    company_id: UUID,
    session: AsyncSession = Depends(get_session),
    quiz_service: QuizService = Depends(QuizService),
    user: User = Depends(get_active_user),
) -> QuizGet:
    return await quiz_service.quiz_create(
        user=user, quiz=quiz, company_id=company_id, session=session
    )


@router.get(
    "/{quiz_id}/get_quiz", response_model=QuizGet, status_code=status.HTTP_200_OK
)
async def quiz_get(
    quiz_id: UUID,
    session: AsyncSession = Depends(get_session),
    quiz_service: QuizService = Depends(QuizService),
    user: User = Depends(get_active_user),
) -> QuizGet:
    return await quiz_service.quiz_get(user=user, quiz_id=quiz_id, session=session)


@router.get(
    "/{company_id}/quiz_list",
    response_model=list[QuizGet],
    status_code=status.HTTP_200_OK,
)
async def quiz_get_list(
    company_id: UUID,
    limit: int,
    offset: int,
    session: AsyncSession = Depends(get_session),
    quiz_service: QuizService = Depends(QuizService),
    user: User = Depends(get_active_user),
) -> list[QuizGet]:
    return await quiz_service.quiz_get_list(
        user=user, company_id=company_id, session=session, limit=limit, offset=offset
    )


@router.patch(
    "/{quiz_id}/update_quiz/{company_id}",
    response_model=QuizGet,
    status_code=status.HTTP_200_OK,
)
async def quiz_update(
    quiz_id: UUID,
    company_id: UUID,
    quiz: QuizUpdate,
    session: AsyncSession = Depends(get_session),
    quiz_service: QuizService = Depends(QuizService),
    user: User = Depends(get_active_user),
) -> QuizGet:
    return await quiz_service.quiz_update(
        user=user, company_id=company_id, session=session, quiz_id=quiz_id, quiz=quiz
    )


@router.delete(
    "/{quiz_id}/delete_quiz/{company_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def quiz_delete(
    quiz_id: UUID,
    company_id: UUID,
    session: AsyncSession = Depends(get_session),
    quiz_service: QuizService = Depends(QuizService),
    user: User = Depends(get_active_user),
) -> None:
    return await quiz_service.quiz_delete(
        user=user, company_id=company_id, session=session, quiz_id=quiz_id
    )
