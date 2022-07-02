import typing


class FiltersRegistry:
    def __init__(self):
        self.filters: list[dict[tuple, typing.Callable]] = []

    def register(self, message_filters: tuple[str], wrapped_function: typing.Callable) -> None:
        self.filters.append({
            message_filters: wrapped_function
        })