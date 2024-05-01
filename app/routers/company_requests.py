from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import RequestsMemberRoles
from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.company_requests import GetInvitation
from app.schemas.user import GetUser
from app.services.auth_jwt import get_active_user
from app.services.company_requests import CompanyRequestsService

company_requests_router = APIRouter(prefix="/company", tags=["Company Requests"])


@company_requests_router.post(
    "/{company_id}/send_invite/{user_id}", status_code=status.HTTP_201_CREATED
)
async def company_send_invite(
    company_id: UUID,
    user_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> GetInvitation:
    return await company_service.company_create_invitation(
        company_id=company_id,
        user_id=user_id,
        user=user,
        session=session,
    )


@company_requests_router.delete(
    "/{company_id}/cancel_invite/{invitation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def company_delete_invite(
    company_id: UUID,
    invitation_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await company_service.company_delete_invitation(
        company_id=company_id, invitation_id=invitation_id, user=user, session=session
    )


@company_requests_router.post(
    "/{company_id}/accept_join_request/{invitation_id}",
    status_code=status.HTTP_200_OK,
)
async def company_accept_join_request(
    company_id: UUID,
    invitation_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await company_service.accept_join_request(
        company_id=company_id, invitation_id=invitation_id, user=user, session=session
    )


@company_requests_router.delete(
    "/{company_id}/reject_join_request/{invitation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def company_reject_join_request(
    company_id: UUID,
    invitation_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await company_service.reject_join_request(
        company_id=company_id, invitation_id=invitation_id, user=user, session=session
    )


@company_requests_router.delete(
    "/{company_id}/kick/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def company_kick_member(
    company_id: UUID,
    user_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await company_service.company_kick_member(
        company_id=company_id, user=user, user_id=user_id, session=session
    )


@company_requests_router.get(
    "/{company_id}/invitations", status_code=status.HTTP_200_OK
)
async def company_invitations(
    company_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetUser]:
    return await company_service.company_invitations_list(
        company_id=company_id, user=user, session=session
    )


@company_requests_router.get(
    "/{company_id}/join_requests", status_code=status.HTTP_200_OK
)
async def company_join_requests(
    company_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetUser]:
    return await company_service.company_join_requests_list(
        company_id=company_id, user=user, session=session
    )


@company_requests_router.get("/{company_id}/members", status_code=status.HTTP_200_OK)
async def company_members(
    company_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetUser]:
    return await company_service.company_get_members(
        company_id=company_id, user=user, session=session
    )


@company_requests_router.post(
    "/{company_id}/update_member_role/{user_id}", status_code=status.HTTP_200_OK
)
async def company_update_member_role(
    company_id: UUID,
    user_id: UUID,
    member_role: str = Depends(RequestsMemberRoles),
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await company_service.company_update_member_role(
        company_id=company_id,
        user_id=user_id,
        user=user,
        session=session,
        member_role=member_role,
    )


@company_requests_router.get("/{company_id}/admins", status_code=status.HTTP_200_OK)
async def company_get_admins_list(
    company_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetUser]:
    return await company_service.company_get_admins_list(
        company_id=company_id, user=user, session=session
    )
