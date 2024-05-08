from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.alchemy.repos.quiz_results import QuizResultsRepos
from app.schemas.quiz_results import QuizResultsCreate, QuizResultsGet


class QuizResultsService:
    def __init__(self):
        self._repo = QuizResultsRepos()

    async def quiz_submit(
        self,
        quiz_results: QuizResultsCreate,
        session: AsyncSession,
        user: User,
        quiz_id: UUID,
        user_id: UUID,
    ) -> QuizResultsGet:
        quiz_results = quiz_results.model_dump()

        return await self._repo.submit_quiz(
            quiz_results=quiz_results,
            session=session,
            quiz_id=quiz_id,
            user_id=user_id,
        )

    async def avg_company_member_score(
        self, session: AsyncSession, user: User, company_id: UUID, user_id: UUID
    ) -> float:
        quiz_results = await self._repo.avg_company_member_score(
            session=session, company_id=company_id, user_id=user_id
        )
        all_questions = 0
        correct_answers = 0
        for result in quiz_results.results:
            all_questions += len(result["questions"])
            for answer in result["questions"]:
                if answer["answer"]["is_correct_answer"]:
                    correct_answers += 1
        result_score = correct_answers / all_questions
        return round(result_score, 1)

    async def avg_user_score(
        self, session: AsyncSession, user: User, user_id: UUID
    ) -> float:
        quiz_results = await self._repo.avg_user_score(session=session, user_id=user_id)
        all_questions = 0
        correct_answers = 0
        for result in quiz_results.results:
            all_questions += len(result["questions"])
            for answer in result["questions"]:
                if answer["answer"]["is_correct_answer"]:
                    correct_answers += 1
        result_score = correct_answers / all_questions
        return round(result_score, 1)
