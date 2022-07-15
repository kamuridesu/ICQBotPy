from .util import CustomDict


class Action(CustomDict):
    def __init__(self) -> None:
        self._looking = "looking"
        self._typing = "typing"

    @property
    def looking(self) -> str:
        return self._looking

    @property
    def typing(self) -> str:
        return self._typing
