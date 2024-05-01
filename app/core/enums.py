import enum


class RequestStatus(enum.Enum):
    MEMBER = "member"
    INVITATIO = "invitation"
    JOIN_REQUEST = "join_request"
    ADMIN = "admin"


class RequestsMemberRoles(enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"
