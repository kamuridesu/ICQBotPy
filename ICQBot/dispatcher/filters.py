import typing


class FiltersRegistry:
    """
    Registry to hold filters and assigned functions
    """
    def __init__(self):
        self.filters: list[dict[tuple, typing.Callable]] = []

    def register(self, message_filters: tuple[str], wrapped_function: typing.Callable) -> None:
        """
        Registers a filter with a function

        :param `message_filters` message filters
        :param `wrapped_function` function to be executed on match
        """
        self.filters.append({
            message_filters: wrapped_function
        })