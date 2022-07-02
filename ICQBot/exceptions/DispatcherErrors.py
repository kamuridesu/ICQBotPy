class DispatcherError(Exception):
    def __init__(self, message: str="An error occured!") -> None:
        super().__init__(message)


class AlreadyPollingError(DispatcherError):
    def __init__(self, message: str="Already Polling!") -> None:
        super().__init__(message)