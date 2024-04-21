from typing import Any
from uuid import UUID


class ObjectNotFound(Exception):
    def __init__(self, id_: Any, model_name: str = "Object") -> None:
        self.msg = f"{model_name} with given identifier - {id_} not found"
        super().__init__(self.msg)


class UserNotFound(ObjectNotFound):
    def __init__(self, id_: UUID, model_name: str = "User") -> None:
        super().__init__(model_name=model_name, id_=id_)
