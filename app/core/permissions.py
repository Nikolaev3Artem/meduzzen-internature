from uuid import UUID

from app.core.exceptions import UserNotAllowed
from app.db.alchemy.models import User


class RoleChecker:
    def check_permission(allowed_user_id: UUID, user: User) -> None:
        if allowed_user_id != user.id:
            raise UserNotAllowed(identifier_=user.id)
