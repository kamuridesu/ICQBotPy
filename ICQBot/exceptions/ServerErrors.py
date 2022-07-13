class ServerError(Exception):
    def __init__(self, message: str="An error ocurred! Probraly server-side, please wait and try again!"):
        super().__init__(message)