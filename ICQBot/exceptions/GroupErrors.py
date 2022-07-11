class GroupError(Exception):
	def __init__(self, message: str="An error occurred while doing this action! Try again!") -> None:
		super().__init__(message)


class CannotRemoveUsersError(GroupError):
    def __init__(self, message: str="An error occurred while tring to remove users from group!") -> None:
        super().__init__(message)
