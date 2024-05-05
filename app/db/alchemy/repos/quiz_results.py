from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import RequestStatus
from app.core.exceptions import MemberNotFound, QuizResultsNotFound
from app.db.alchemy.models import CompanyRequests, QuizResults
from app.schemas.quiz_results import QuizResultsCreate, QuizResultsGet


class QuizResultsRepos:
    @staticmethod
    async def submit_quiz(
        quiz_results: QuizResultsCreate,
        session: AsyncSession,
        company_id: UUID,
        quiz_id: UUID,
        user_id: UUID,
    ) -> QuizResultsGet:
        quiz_result = await session.execute(
            select(QuizResults).where(
                QuizResults.company_id == company_id,
                QuizResults.user_id == user_id,
                QuizResults.quiz_id == quiz_id,
            )
        )
        quiz_result = quiz_result.scalar()
        if quiz_result is not None:
            quiz_result.results = quiz_result.results + quiz_results["results"]
        else:
            quiz_result = QuizResults(
                company_id=company_id,
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
        check_member_exists = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.user_id == user_id,
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.MEMBER.value,
            )
        )
        if check_member_exists.scalar() is None:
            raise MemberNotFound(identifier_=user_id)

        quiz_results = await session.execute(
            select(QuizResults).where(
                QuizResults.user_id == user_id, QuizResults.company_id == company_id
            )
        )
        quiz_results = quiz_results.scalar()
        if quiz_results is None:
            raise QuizResultsNotFound(identifier_=user_id)
        all_questions = 0
        correct_answers = 0
        for result in quiz_results.results:
            all_questions += len(result["answers"])
            for i in result["answers"]:
                if i["is_correct_answer"]:
                    correct_answers += 1
        result_score = correct_answers / all_questions
        return round(result_score, 1)

    @staticmethod
    async def avg_user_score(session: AsyncSession, user_id: UUID) -> float:
        quiz_results = await session.execute(
            select(QuizResults).where(QuizResults.user_id == user_id)
        )
        quiz_results = quiz_results.scalar()
        if quiz_results is None:
            raise QuizResultsNotFound(identifier_=user_id)
        all_questions = 0
        correct_answers = 0
        for result in quiz_results.results:
            all_questions += len(result["answers"])
            for answer in result["answers"]:
                if answer["is_correct_answer"]:
                    correct_answers += 1
        result_score = correct_answers / all_questions
        return round(result_score, 1)
