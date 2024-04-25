from typing import Any


class ObjectNotFound(Exception):
    def __init__(self, identifier_: Any, model_name: str = "Object") -> None:
        self.msg = f"{model_name} with given identifier - {identifier_} not found"
        super().__init__(self.msg)


class UserNotFound(ObjectNotFound):
    def __init__(self, identifier_: str, model_name: str = "User") -> None:
        super().__init__(model_name=model_name, identifier_=identifier_)


class CompanyNotFound(ObjectNotFound):
    def __init__(self, identifier_: str, model_name: str = "Company") -> None:
        super().__init__(model_name=model_name, identifier_=identifier_)


class NotAllowed(Exception):
    def __init__(self, identifier_: Any, model_name: str = "Object") -> None:
        self.msg = f"{model_name} with given identifier - {identifier_} not permitted to do this action"
        super().__init__(self.msg)


class UserNotAllowed(NotAllowed):
    def __init__(self, identifier_: str, model_name: str = "User") -> None:
        super().__init__(model_name=model_name, identifier_=identifier_)


class NotAuthorized(Exception):
    def __init__(self) -> None:
        self.msg = "Username or password is incorrect"
        super().__init__(self.msg)
