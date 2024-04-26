from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvitationNotFound, UserNotFound
from app.core.hashing import Hasher
from app.db.alchemy.models import CompanyRequests, RequestStatus, User
from app.schemas.user import (
    CreateJoinRequest,
    GetInvitation,
    GetJoinRequest,
    GetUser,
    UserSignUp,
    UserUpdate,
)


class UserRepos:
    @staticmethod
    async def create_user(user: UserSignUp, session: AsyncSession) -> User:
        user = User(
            email=user.email,
            password=Hasher.get_password_hash(user.password),
            username=user.username,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def list_users(limit: int, offset: int, session: AsyncSession) -> list[User]:
        users_list = await session.execute(
            select(User).where(User.is_active == True).limit(limit).offset(offset)
        )
        return users_list.scalars().all()

    @staticmethod
    async def get_user(id: UUID, session: AsyncSession) -> User:
        user_data = await session.get(User, id)
        if not user_data or not user_data.is_active:
            raise UserNotFound(identifier_=id)
        return user_data

    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession) -> User:
        user_data = await session.execute(select(User).where(User.email == email))
        user_data = user_data.scalar()
        if not user_data or not user_data.is_active:
            raise UserNotFound(identifier_=email)
        return user_data

    @staticmethod
    async def deactivate_user(user_id: UUID, session: AsyncSession) -> None:
        user_data = await session.get(User, user_id)
        if not user_data or not user_data.is_active:
            raise UserNotFound(identifier_=user_id)
        user_data.is_active = False
        await session.commit()

    @staticmethod
    async def update_user(
        user_id: UUID, user_data: UserUpdate, session: AsyncSession
    ) -> GetUser:
        user_in_db = await session.get(User, user_id)
        if not user_in_db or not user_in_db.is_active:
            raise UserNotFound(identifier_=user_id)
        user_data = user_data.model_dump(exclude_unset=True)

        for key, value in user_data.items():
            setattr(user_in_db, key, value)

        await session.commit()
        return user_in_db

    @staticmethod
    async def get_invitation_user(
        invitation_id: UUID, session: AsyncSession
    ) -> GetInvitation:
        invitations_list = await session.get(CompanyRequests, invitation_id)
        return invitations_list

    @staticmethod
    async def invitation_list_user(
        user_id: UUID, session: AsyncSession
    ) -> list[GetInvitation]:
        invitations_list = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.user_id == user_id,
                CompanyRequests.status == RequestStatus.INVITATION,
            )
        )
        return invitations_list.scalars().all()

    @staticmethod
    async def accept_invitation_user(
        invitation_id: UUID, session: AsyncSession
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)
        invitation.status = RequestStatus.MEMBER
        await session.commit()

    @staticmethod
    async def reject_invitation_user(
        invitation_id: UUID, session: AsyncSession
    ) -> None:
        invitation = await session.get(CompanyRequests, invitation_id)
        if not invitation:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(invitation)
        await session.commit()

    @staticmethod
    async def user_create_join_request(
        user_id: UUID, session: AsyncSession, create_join_request: CreateJoinRequest
    ) -> GetJoinRequest:
        user_join_request = CompanyRequests(
            company_id=create_join_request.company_id,
            user_id=user_id,
            status=RequestStatus.JOIN_REQUEST,
        )
        session.add(user_join_request)
        await session.commit()
        await session.refresh(user_join_request)
        return user_join_request

    @staticmethod
    async def user_list_join_request(
        user_id: UUID, session: AsyncSession
    ) -> list[GetJoinRequest]:
        invitations_list = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.user_id == user_id,
                CompanyRequests.status == RequestStatus.JOIN_REQUEST,
            )
        )
        return invitations_list.scalars().all()

    @staticmethod
    async def user_cancel_join_request(
        invitation_id: UUID, session: AsyncSession
    ) -> None:
        join_request = await session.get(CompanyRequests, invitation_id)
        if not join_request:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(join_request)
        await session.commit()

    @staticmethod
    async def user_company_leave(invitation_id: UUID, session: AsyncSession) -> None:
        join_request = await session.execute(
            select(CompanyRequests).where(
                CompanyRequests.id == invitation_id,
                CompanyRequests.status == RequestStatus.MEMBER,
            )
        )
        if not join_request:
            raise InvitationNotFound(identifier_=invitation_id)

        await session.delete(join_request.scalar())
        await session.commit()
