import enum


class RequestStatus(enum.Enum):
    MEMBER = "member"
    INVITATION = "invitation"
    JOIN_REQUEST = "join_request"
