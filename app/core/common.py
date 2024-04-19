from fastapi import HTTPException


class ObjNotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "Object not found"


class UserNotFound(ObjNotFound):
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "User not found"
