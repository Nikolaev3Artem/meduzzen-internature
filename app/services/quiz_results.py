import pickle
from uuid import UUID

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.alchemy.repos.company import CompanyRepos
from app.db.alchemy.repos.quiz import QuizRepos
from app.db.alchemy.repos.quiz_results import QuizResultsRepos
from app.db.alchemy.repos.user import UserRepos
from app.schemas.quiz_results import QuizResultsCreate, QuizResultsGet


class QuizResultsService:
    def __init__(self):
        self._repo = QuizResultsRepos()
        self._user_repo = UserRepos()
        self._company_repo = CompanyRepos()
        self._quiz_repo = QuizRepos()

    async def quiz_submit(
        self,
        quiz_results: QuizResultsCreate,
        session: AsyncSession,
        user: User,
        company_id: UUID,
        quiz_id: UUID,
        user_id: UUID,
        redis_service: redis,
    ) -> QuizResultsGet:
        quiz_results = quiz_results.model_dump()
        user_data = await self._user_repo.get_user(id=user_id, session=session)
        company_data = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        quiz_data = await self._quiz_repo.get_quiz(
            quiz_id=quiz_id, company_id=company_id, session=session
        )

        redis_data = {
            "User": user_data,
            "Company": company_data,
            "QuizResults": quiz_results,
            "Quiz": quiz_data,
        }
        await redis_service.set_cache("User_Data", pickle.dumps(redis_data))

        return await self._repo.submit_quiz(
            quiz_results=quiz_results,
            session=session,
            company_id=company_id,
            quiz_id=quiz_id,
            user_id=user_id,
        )

    async def avg_company_member_score(
        self, session: AsyncSession, user: User, company_id: UUID, user_id: UUID
    ) -> float:
        return await self._repo.avg_company_member_score(
            session=session, company_id=company_id, user_id=user_id
        )

    async def avg_user_score(
        self, session: AsyncSession, user: User, user_id: UUID
    ) -> float:
        return await self._repo.avg_user_score(session=session, user_id=user_id)
