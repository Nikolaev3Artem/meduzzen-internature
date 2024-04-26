from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CompanyNotFound, InvitationNotFound
from app.db.alchemy.models import Company, CompanyRequests, RequestStatus, User
from app.schemas.company import (
    CompanyCreate,
    CompanyGet,
    CompanyUpdate,
    CreateInvitation,
    GetInvitation,
)
from app.schemas.user import GetJoinRequest


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

    @staticmethod
    async def company_create_invitation(
        company_id: UUID, session: AsyncSession, create_invitation: CreateInvitation
    ) -> None:
        company_data = await session.get(Company, company_id)
        if not company_data or not company_data.visible:
            raise CompanyNotFound(identifier_=company_id)

        company_request = CompanyRequests(
            company_id=company_id,
            user_id=create_invitation.user_id,
            status=RequestStatus.INVITATION,
        )
        session.add(company_request)
        await session.commit()
        await session.refresh(company_request)
        return company_request

    @staticmethod
    async def company_delete_invitation(
        session: AsyncSession, invitation_id: UUID
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)

        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)

        if invitation.status != RequestStatus.MEMBER:
            await session.delete(invitation)
            await session.commit()

    @staticmethod
    async def invitations_list_company(
        company_id: UUID, session: AsyncSession
    ) -> list[CompanyGet]:
        invitations_list = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.INVITATION,
            )
        )
        return invitations_list.scalars().all()

    @staticmethod
    async def company_get_members(
        company_id: UUID, session: AsyncSession
    ) -> list[GetInvitation]:
        members_list = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.MEMBER,
            )
        )
        return members_list.scalars().all()

    @staticmethod
    async def company_kick_member(
        company_id: UUID, session: AsyncSession, user_id: UUID
    ) -> None:
        member = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.user_id == user_id,
                CompanyRequests.status == RequestStatus.MEMBER,
            )
        )
        await session.delete(member.scalar())
        await session.commit()

    @staticmethod
    async def company_join_requests_list(
        company_id: UUID, session: AsyncSession
    ) -> list[GetJoinRequest]:
        join_requests_list = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.company_id == company_id,
                CompanyRequests.status == RequestStatus.JOIN_REQUEST,
            )
        )
        return join_requests_list.scalars().all()

    @staticmethod
    async def company_accept_join_request(
        session: AsyncSession, invitation_id: UUID
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)
        invitation.status = RequestStatus.MEMBER
        await session.commit()

    @staticmethod
    async def company_reject_join_request(
        session: AsyncSession, invitation_id: UUID
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(invitation)
        await session.commit()
