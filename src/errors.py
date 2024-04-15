


class CreateDBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class GetDBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class GetManyDBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class UpdateDBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DeleteDBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DBServiceException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(*message)


class FieldValidationException(ValueError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
