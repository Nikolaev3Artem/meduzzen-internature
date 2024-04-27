from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import RoleChecker
from app.db.alchemy.models import User
from app.db.alchemy.repos.company import CompanyRepos
from app.schemas.company import CompanyCreate, CompanyGet, CompanyUpdate


class CompanyService:
    def __init__(self):
        self._repo = CompanyRepos()

    async def company_create(
        self, company: CompanyCreate, session: AsyncSession, user: User
    ) -> CompanyGet:
        return await self._repo.create_company(
            company=company, session=session, user=user
        )

    async def companies_list(
        self, limit: int, offset: int, session: AsyncSession
    ) -> list[CompanyGet]:
        return await self._repo.list_companies(
            limit=limit, offset=offset, session=session
        )

    async def company_get(self, id: UUID, session: AsyncSession) -> CompanyGet:
        return await self._repo.get_company(id=id, session=session, get_hidden=False)

    async def company_update(
        self,
        company_id: UUID,
        company_data: CompanyUpdate,
        session: AsyncSession,
        user: User,
    ) -> CompanyGet:
        company = await self._repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.update_company(
            company_id=company_id, company_data=company_data, session=session
        )

    async def company_deactivate(
        self, company_id: UUID, session: AsyncSession, user: User
    ) -> None:
        company = await self._repo.get_company(
            id=company_id, session=session, get_hidden=True
        )
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)

        return await self._repo.deactivate_company(
            company_id=company_id, session=session
        )
