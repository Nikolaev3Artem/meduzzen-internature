from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import QuizResultsNotFound
from app.db.alchemy.models import QuizResults
from app.schemas.quiz_results import QuizResultsCreate, QuizResultsGet


class QuizResultsRepos:
    @staticmethod
    async def submit_quiz(
        quiz_results: QuizResultsCreate,
        session: AsyncSession,
        quiz_id: UUID,
        user_id: UUID,
    ) -> QuizResultsGet:
        quiz_result = await session.execute(
            select(QuizResults).where(
                QuizResults.company_id == quiz_results["company_id"],
                QuizResults.user_id == user_id,
                QuizResults.quiz_id == quiz_id,
            )
        )
        quiz_result = quiz_result.scalar()
        if quiz_result is not None:
            quiz_result.results = quiz_result.results + quiz_results["results"]
        else:
            quiz_result = QuizResults(
                company_id=quiz_results["company_id"],
                user_id=user_id,
                quiz_id=quiz_id,
                results=quiz_results["results"],
            )

            session.add(quiz_result)
        await session.commit()
        await session.refresh(quiz_result)
        return quiz_result

    @staticmethod
    async def avg_company_member_score(
        session: AsyncSession, company_id: UUID, user_id: UUID
    ) -> float:
        quiz_results = await session.execute(
            select(QuizResults).where(
                QuizResults.user_id == user_id, QuizResults.company_id == company_id
            )
        )
        quiz_results = quiz_results.scalar()
        if quiz_results is None:
            raise QuizResultsNotFound(identifier_=user_id)
        return quiz_results

    @staticmethod
    async def avg_user_score(session: AsyncSession, user_id: UUID) -> float:
        quiz_results = await session.execute(
            select(QuizResults).where(QuizResults.user_id == user_id)
        )

        quiz_results = quiz_results.scalar()
        if quiz_results is None:
            raise QuizResultsNotFound(identifier_=user_id)
        return quiz_results
