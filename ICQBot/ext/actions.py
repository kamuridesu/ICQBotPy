from .util import CustomDict


class Action(CustomDict):
    def __init__(self, action:str) -> None:
        if action.lower() not in ["looking", "typing"]:
            raise TypeError("Action must be either 'looking' or 'typing'")
        self.action = action.lower()
