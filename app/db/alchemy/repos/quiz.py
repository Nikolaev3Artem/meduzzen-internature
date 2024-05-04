from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import QuizNotFound
from app.db.alchemy.models import Quiz
from app.schemas.quiz import QuizCreate, QuizGet, QuizUpdate


class QuizRepos:
    @staticmethod
    async def create_quiz(
        quiz: QuizCreate, session: AsyncSession, company_id: UUID
    ) -> QuizGet:
        quiz = Quiz(
            name=quiz["name"],
            description=quiz["description"],
            questions=quiz["questions"],
            company_id=company_id,
        )
        session.add(quiz)
        await session.commit()
        await session.refresh(quiz)
        return quiz

    @staticmethod
    async def get_quiz(quiz_id: UUID, session: AsyncSession) -> QuizGet:
        quiz_data = await session.get(Quiz, quiz_id)
        if not quiz_data:
            raise QuizNotFound(identifier_=quiz_id)
        return quiz_data

    @staticmethod
    async def get_list_quiz(
        company_id: UUID, session: AsyncSession, limit: int, offset: int
    ) -> list[QuizGet]:
        quiz_data = await session.execute(
            select(Quiz)
            .where(Quiz.company_id == company_id)
            .limit(limit)
            .offset(offset)
        )
        quiz_data = quiz_data.scalars().all()
        if not quiz_data:
            raise QuizNotFound(identifier_=company_id)
        return quiz_data

    @staticmethod
    async def update_quiz(
        company_id: UUID, session: AsyncSession, quiz_id: UUID, quiz: QuizUpdate
    ) -> QuizGet:
        quiz_data = await session.execute(
            select(Quiz).where(Quiz.company_id == company_id, Quiz.id == quiz_id)
        )
        quiz_data = quiz_data.scalar()
        if not quiz_data:
            raise QuizNotFound(identifier_=quiz_id)
        for key, value in quiz.items():
            setattr(quiz_data, key, value)

        await session.commit()
        return quiz_data

    @staticmethod
    async def delete_quiz(
        company_id: UUID, session: AsyncSession, quiz_id: UUID
    ) -> None:
        quiz_data = await session.execute(
            select(Quiz).where(Quiz.company_id == company_id, Quiz.id == quiz_id)
        )
        quiz_data = quiz_data.scalar()
        if not quiz_data:
            raise QuizNotFound(identifier_=quiz_id)

        await session.delete(quiz_data)
        await session.commit()
