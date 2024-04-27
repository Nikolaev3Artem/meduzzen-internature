from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.company import GetInvitation
from app.schemas.user import GetJoinRequest
from app.services.auth_jwt import get_active_user
from app.services.company_requests import CompanyRequestsService
from app.services.user import UserService

company_requests_router = APIRouter(prefix="/company", tags=["Company Requests"])
user_requests_router = APIRouter(prefix="/user", tags=["User Requests"])


@company_requests_router.post("/{company_id}/{user_id}/send_invite")
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
    "/{company_id}/{invitation_id}/cancel_invite",
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


@company_requests_router.post("/{company_id}/{invitation_id}/accept_join_request")
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
    "/{company_id}/{invitation_id}/reject_join_request",
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
    "/{company_id}/{user_id}/kick", status_code=status.HTTP_204_NO_CONTENT
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


@company_requests_router.get("/{company_id}/invitations")
async def company_invitations(
    company_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetInvitation]:
    return await company_service.company_invitations_list(
        company_id=company_id, user=user, session=session
    )


@company_requests_router.get("/{company_id}/join_requests")
async def company_join_requests(
    company_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetJoinRequest]:
    return await company_service.company_join_requests_list(
        company_id=company_id, user=user, session=session
    )


@company_requests_router.get("/{company_id}/members")
async def company_members(
    company_id: UUID,
    company_service: CompanyRequestsService = Depends(CompanyRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetInvitation]:
    return await company_service.company_get_members(
        company_id=company_id, user=user, session=session
    )


@user_requests_router.post("/{invitation_id}/accept_invitation")
async def user_accept_invitation(
    invitation_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_accept_invitation(
        invitation_id=invitation_id, session=session, user=user
    )


@user_requests_router.delete(
    "/{invitation_id}/reject_invitation", status_code=status.HTTP_204_NO_CONTENT
)
async def user_reject_invitation(
    invitation_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_reject_invitation(
        invitation_id=invitation_id, session=session, user=user
    )


@user_requests_router.post("/{company_id}/send_join_request")
async def user_send_join_request(
    company_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> GetJoinRequest:
    return await user_service.user_create_join_request(
        user_id=user.id,
        company_id=company_id,
        user=user,
        session=session,
    )


@user_requests_router.delete(
    "/cancel_join_request/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def user_cancel_join_request(
    invitation_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_cancel_join_request(
        invitation_id=invitation_id, user=user, session=session
    )


@user_requests_router.delete(
    "/{company_id}/leave/", status_code=status.HTTP_204_NO_CONTENT
)
async def user_leave_company(
    invitation_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_company_leave(
        invitation_id=invitation_id, user=user, session=session
    )


@user_requests_router.get("/invitations")
async def user_invitations(
    user_id: UUID,
    user_service: UserService = Depends(UserService),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_active_user),
) -> list[GetInvitation]:
    return await user_service.user_invitation_list(
        user_id=user_id, session=session, user=user
    )


@user_requests_router.get("/join_requests")
async def user_join_requests(
    user_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetJoinRequest]:
    return await user_service.user_list_join_request(
        user_id=user_id, user=user, session=session
    )
