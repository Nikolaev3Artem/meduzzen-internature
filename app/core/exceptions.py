from typing import Any


class ObjectNotFound(Exception):
    def __init__(self, identifier_: Any, model_name: str = "Object") -> None:
        self.msg = f"{model_name} with given identifier - {identifier_} not found"
        super().__init__(self.msg)


class IntegritiError(Exception):
    def __init__(
        self, input_data_: Any, column_name_: str, model_name: str = "Object"
    ) -> None:
        self.msg = f"Can not create {model_name} with {column_name_} = {input_data_}, already exists"
        super().__init__(self.msg)


class CompanyNameAlreadyExists(IntegritiError):
    def __init__(
        self, input_data_: str, column_name_: str, model_name: str = "Company"
    ) -> None:
        super().__init__(
            model_name=model_name, column_name_=column_name_, input_data_=input_data_
        )


class InvitationAlreadyExists(IntegritiError):
    def __init__(
        self, input_data_: str, column_name_: str, model_name: str = "Invitation"
    ) -> None:
        super().__init__(
            model_name=model_name, column_name_=column_name_, input_data_=input_data_
        )


class UserNotFound(ObjectNotFound):
    def __init__(self, identifier_: str, model_name: str = "User") -> None:
        super().__init__(model_name=model_name, identifier_=identifier_)


class MemberNotFound(ObjectNotFound):
    def __init__(self, identifier_: str, model_name: str = "Company Member") -> None:
        super().__init__(model_name=model_name, identifier_=identifier_)


class CompanyNotFound(ObjectNotFound):
    def __init__(self, identifier_: str, model_name: str = "Company") -> None:
        super().__init__(model_name=model_name, identifier_=identifier_)


class InvitationNotFound(ObjectNotFound):
    def __init__(self, identifier_: str, model_name: str = "CompanyRequests") -> None:
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
