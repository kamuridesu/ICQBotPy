import typing


class ClientError(Exception):
    def __init__(self, message: str="") -> None:
        super().__init__(message)


class ResourceNotFoundError(ClientError):
    def __init__(self, message: str="Resource not Found!") -> None:
        super().__init__(message)


class BadRequestError(ClientError):
    def __init__(self, message: str="Server did not understand the request!") -> None:
        super().__init__(message)


class UnauthorizedError(ClientError):
    def __init__(self, message: str="Client do not have rights to access the resource!") -> None:
        super().__init__(message)


class InvalidTokenError(UnauthorizedError):
    def __init__(self, message: str="Please, check if your token is valid and try again or generate a new one!") -> None:
        super().__init__(message)
