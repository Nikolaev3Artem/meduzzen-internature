from uuid import UUID

from app.core.exceptions import UserNotAllowed
from app.db.alchemy.models import User


class RoleChecker:
    async def check_permission(self, allowed_user_id: UUID, user: User) -> bool:
        if allowed_user_id == user.id:
            return True
        raise UserNotAllowed(identifier_=user.id)
