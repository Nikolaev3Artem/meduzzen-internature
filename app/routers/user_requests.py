from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.user import GetJoinRequest, GetUser
from app.services.auth_jwt import get_active_user
from app.services.user_requests import UserRequestsService

user_requests_router = APIRouter(prefix="/user", tags=["User Requests"])


@user_requests_router.post(
    "/{invitation_id}/accept_invite", status_code=status.HTTP_201_CREATED
)
async def user_accept_invitation(
    invitation_id: UUID,
    user_service: UserRequestsService = Depends(UserRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_accept_invitation(
        invitation_id=invitation_id, session=session, user=user
    )


@user_requests_router.delete(
    "/{invitation_id}/reject_invite", status_code=status.HTTP_204_NO_CONTENT
)
async def user_reject_invitation(
    invitation_id: UUID,
    user_service: UserRequestsService = Depends(UserRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_reject_invitation(
        invitation_id=invitation_id, session=session, user=user
    )


@user_requests_router.post(
    "/{company_id}/send_join_request", status_code=status.HTTP_201_CREATED
)
async def user_send_join_request(
    company_id: UUID,
    user_service: UserRequestsService = Depends(UserRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> GetJoinRequest:
    return await user_service.user_create_join_request(
        company_id=company_id,
        user=user,
        session=session,
    )


@user_requests_router.delete(
    "/cancel_join_request/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def user_cancel_join_request(
    invitation_id: UUID,
    user_service: UserRequestsService = Depends(UserRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_cancel_join_request(
        invitation_id=invitation_id, user=user, session=session
    )


@user_requests_router.delete(
    "/{company_id}/leave", status_code=status.HTTP_204_NO_CONTENT
)
async def user_leave_company(
    company_id: UUID,
    user_service: UserRequestsService = Depends(UserRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_company_leave(
        company_id=company_id, user=user, session=session
    )


@user_requests_router.get("/{user_id}/invites", status_code=status.HTTP_200_OK)
async def user_invitations(
    user_id: UUID,
    user_service: UserRequestsService = Depends(UserRequestsService),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_active_user),
) -> list[GetUser]:
    return await user_service.user_invitation_list(
        session=session, user=user, user_id=user_id
    )


@user_requests_router.get("/{user_id}/join_requests", status_code=status.HTTP_200_OK)
async def user_join_requests(
    user_id: UUID,
    user_service: UserRequestsService = Depends(UserRequestsService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetUser]:
    return await user_service.user_list_join_request(
        user_id=user_id, user=user, session=session
    )
