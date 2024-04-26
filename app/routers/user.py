from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.alchemy.models import User
from app.db.postgress import get_session
from app.schemas.user import (
    CreateJoinRequest,
    GetInvitation,
    GetJoinRequest,
    GetUser,
    UserSignUp,
    UserUpdate,
)
from app.services.auth_jwt import get_active_user
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", response_model=UserSignUp, status_code=status.HTTP_201_CREATED)
async def user_create(
    user: UserSignUp,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
) -> GetUser:
    return await user_service.user_create(user=user, session=session)


@router.get("/", response_model=list[GetUser])
async def users_list(
    limit: int,
    offset: int,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
) -> list[GetUser]:
    return await user_service.users_list(limit=limit, offset=offset, session=session)


@router.get("/{user_id}", response_model=GetUser)
async def user_get(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
) -> GetUser:
    return await user_service.user_get(id=user_id, session=session)


@router.patch("/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
async def user_deactivate(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
) -> None:
    return await user_service.user_deactivate(
        user_id=user_id, session=session, user=user
    )


@router.patch("/{user_id}", response_model=UserUpdate)
async def user_update(
    user_id: UUID,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
):
    return await user_service.user_update(
        user_id=user_id, user_data=user_data, session=session, user=user
    )


@router.post("/accept_invitation/{invitation_id}")
async def user_accept_invitation(
    invitation_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_accept_invitation(
        invitation_id=invitation_id, session=session, user=user
    )


@router.delete(
    "/reject_invitation/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT
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


@router.post("/{user_id}/send_join_request/")
async def user_send_join_request(
    user_id: UUID,
    create_join_request: CreateJoinRequest,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> GetJoinRequest:
    return await user_service.user_create_join_request(
        user_id=user_id,
        create_join_request=create_join_request,
        user=user,
        session=session,
    )


@router.delete(
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


@router.delete("/leave/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def user_leave_company(
    invitation_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    return await user_service.user_company_leave(
        invitation_id=invitation_id, user=user, session=session
    )


@router.get("/{user_id}/invitations")
async def user_invitations(
    user_id: UUID,
    user_service: UserService = Depends(UserService),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_active_user),
) -> list[GetInvitation]:
    return await user_service.user_invitation_list(
        user_id=user_id, session=session, user=user
    )


@router.get("/{user_id}/join_requests")
async def user_join_requests(
    user_id: UUID,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_active_user),
    session: AsyncSession = Depends(get_session),
) -> list[GetJoinRequest]:
    return await user_service.user_list_join_request(
        user_id=user_id, user=user, session=session
    )
