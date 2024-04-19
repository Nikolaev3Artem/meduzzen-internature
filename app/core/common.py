class ObjNotFoundException(Exception):
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "Object not found"
