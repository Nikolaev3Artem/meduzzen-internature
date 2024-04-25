from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CompanyNotFound
from app.db.alchemy.models import Company, User
from app.schemas.company import CompanyCreate, CompanyGet, CompanyUpdate


class CompanyRepos:
    @staticmethod
    async def create_company(
        company: CompanyCreate, session: AsyncSession, user: User
    ) -> CompanyGet:
        company = Company(
            owner_id=user.id,
            name=company.name,
            description=company.description,
        )
        session.add(company)
        await session.commit()
        await session.refresh(company)
        return company

    @staticmethod
    async def list_companies(
        limit: int, offset: int, session: AsyncSession
    ) -> list[CompanyGet]:
        companies_list = await session.execute(
            select(Company).where(Company.visible == True).limit(limit).offset(offset)
        )
        return companies_list.scalars().all()

    @staticmethod
    async def get_company(id: UUID, session: AsyncSession) -> CompanyGet:
        company_data = await session.get(Company, id)
        if not company_data or not company_data.visible:
            raise CompanyNotFound(identifier_=id)
        return company_data

    @staticmethod
    async def update_company(
        company_id: UUID, company_data: CompanyUpdate, session: AsyncSession, user: User
    ) -> CompanyGet:
        company_in_db = await session.get(Company, company_id)

        if not company_in_db:
            raise CompanyNotFound(identifier_=company_id)

        company_data = company_data.model_dump(exclude_unset=True)

        for key, value in company_data.items():
            setattr(company_in_db, key, value)

        await session.commit()
        return company_in_db

    @staticmethod
    async def deactivate_company(company_id: UUID, session: AsyncSession) -> None:
        company_data = await session.get(Company, company_id)
        if not company_data or not company_data.visible:
            raise CompanyNotFound(identifier_=company_id)
        company_data.visible = False
        await session.commit()
