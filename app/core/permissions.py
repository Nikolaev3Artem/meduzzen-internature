from uuid import UUID

from app.core.exceptions import UserNotAllowed
from app.db.alchemy.models import User


class RoleChecker:
    def check_owner(allowed_user_id: UUID, user: User) -> None:
        if allowed_user_id != user.id:
            raise UserNotAllowed(identifier_=user.id)

    def check_superstaff(allowed_users: list, user: User, owner_id: UUID) -> None:
        if user in allowed_users or owner_id == user.id:
            return
        raise UserNotAllowed(identifier_=user.id)
