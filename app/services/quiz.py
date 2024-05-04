from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import RoleChecker
from app.db.alchemy.models import User
from app.db.alchemy.repos.company import CompanyRepos
from app.db.alchemy.repos.company_requests import CompanyRequestsRepos
from app.db.alchemy.repos.quiz import QuizRepos
from app.schemas.quiz import QuizCreate, QuizGet, QuizUpdate


class QuizService:
    def __init__(self):
        self._repo = QuizRepos()
        self._company_repo = CompanyRepos()
        self._company_requests_repo = CompanyRequestsRepos()

    async def quiz_create(
        self, quiz: QuizCreate, company_id: UUID, session: AsyncSession, user: User
    ) -> QuizGet:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        admins_list = await self._company_requests_repo.company_get_admins_list(
            company_id=company_id, session=session
        )
        RoleChecker.check_superstaff(
            allowed_users=admins_list, user=user, owner_id=company.owner_id
        )
        quiz = quiz.model_dump()
        return await self._repo.create_quiz(
            quiz=quiz, session=session, company_id=company_id
        )

    async def quiz_get(
        self, quiz_id: UUID, session: AsyncSession, user: User
    ) -> QuizGet:
        return await self._repo.get_quiz(quiz_id=quiz_id, session=session)

    async def quiz_get_list(
        self,
        company_id: UUID,
        session: AsyncSession,
        user: User,
        limit: int,
        offset: int,
    ) -> list[QuizGet]:
        return await self._repo.get_list_quiz(
            company_id=company_id, session=session, limit=limit, offset=offset
        )

    async def quiz_update(
        self,
        company_id: UUID,
        session: AsyncSession,
        user: User,
        quiz: QuizUpdate,
        quiz_id: UUID,
    ) -> QuizGet:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        admins_list = await self._company_requests_repo.company_get_admins_list(
            company_id=company_id, session=session
        )
        RoleChecker.check_superstaff(
            allowed_users=admins_list, user=user, owner_id=company.owner_id
        )
        quiz = quiz.model_dump(exclude_unset=True)
        return await self._repo.update_quiz(
            company_id=company_id, session=session, quiz=quiz, quiz_id=quiz_id
        )

    async def quiz_delete(
        self, company_id: UUID, session: AsyncSession, user: User, quiz_id: UUID
    ) -> None:
        company = await self._company_repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        admins_list = await self._company_requests_repo.company_get_admins_list(
            company_id=company_id, session=session
        )
        RoleChecker.check_superstaff(
            allowed_users=admins_list, user=user, owner_id=company.owner_id
        )
        return await self._repo.delete_quiz(
            company_id=company_id, session=session, quiz_id=quiz_id
        )
