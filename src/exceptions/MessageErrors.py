class MessageNotSentError(Exception):
	def __init__(self, message: str="The message could not be found! Please, try again!") -> None:
		super().__init__(message)


class AmbigousFileError(MessageNotSentError):
	def __init__(self, message: str="Cannot send with file_id and file selected at same time, choose one!") -> None:
		super().__init__(message)