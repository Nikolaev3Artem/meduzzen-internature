import enum


class RequestStatus(enum.Enum):
    MEMBER = "Member"
    INVITATION = "Invitation"
    JOIN_REQUEST = "Join_Request"
    ADMIN = "Admin"
