from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import RoleChecker
from app.db.alchemy.models import User
from app.db.alchemy.repos.company import CompanyRepos
from app.schemas.company import (
    CompanyCreate,
    CompanyGet,
    CompanyUpdate,
    CreateInvitation,
    GetInvitation,
)
from app.schemas.user import GetJoinRequest


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

    async def company_create_invitation(
        self,
        company_id: UUID,
        create_invitation: CreateInvitation,
        user: User,
        session: AsyncSession,
    ) -> GetInvitation:
        company = await CompanyService.company_get(self, id=company_id, session=session)
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)

        return await self._repo.company_create_invitation(
            company_id=company_id, session=session, create_invitation=create_invitation
        )

    async def company_delete_invitation(
        self, company_id: UUID, invitation_id: UUID, user: User, session: AsyncSession
    ) -> GetInvitation:
        company = await CompanyService.company_get(self, id=company_id, session=session)

        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)

        return await self._repo.company_delete_invitation(
            session=session, invitation_id=invitation_id
        )

    async def company_invitations_list(
        self, user: User, company_id: UUID, session: AsyncSession
    ) -> list[GetInvitation]:
        company = await CompanyService.company_get(self, id=company_id, session=session)
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.invitations_list_company(
            company_id=company_id, session=session
        )

    async def company_get_members(
        self, user: User, company_id: UUID, session: AsyncSession
    ) -> list[GetInvitation]:
        company = await CompanyService.company_get(self, id=company_id, session=session)
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_get_members(
            company_id=company_id, session=session
        )

    async def company_kick_member(
        self, user: User, user_id: UUID, company_id: UUID, session: AsyncSession
    ) -> list[GetInvitation]:
        company = await CompanyService.company_get(self, id=company_id, session=session)
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_kick_member(
            company_id=company_id, session=session, user_id=user_id
        )

    async def company_join_requests_list(
        self, user: User, company_id: UUID, session: AsyncSession
    ) -> list[GetJoinRequest]:
        company = await CompanyService.company_get(self, id=company_id, session=session)
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_join_requests_list(
            company_id=company_id, session=session
        )

    async def accept_join_request(
        self, user: User, company_id: UUID, invitation_id: UUID, session: AsyncSession
    ) -> None:
        company = await CompanyService.company_get(self, id=company_id, session=session)
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_accept_join_request(
            session=session, invitation_id=invitation_id
        )

    async def reject_join_request(
        self, user: User, company_id: UUID, invitation_id: UUID, session: AsyncSession
    ) -> None:
        company = await CompanyService.company_get(self, id=company_id, session=session)
        RoleChecker.check_permission(allowed_user_id=company.owner_id, user=user)
        return await self._repo.company_reject_join_request(
            session=session, invitation_id=invitation_id
        )
