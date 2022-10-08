import typing


class FiltersRegistry:
    """
    Registry to hold filters and assigned functions
    """

    def __init__(self):
        self.message_filters: list[dict[tuple, typing.Callable]] = []
        self.edited_message_filters: list[dict[tuple, typing.Callable]] = []
        self.deleted_message_filters: list[dict[tuple, typing.Callable]] = []
        self.callback_filters: list[
            dict[str, typing.Union[str, typing.Callable, typing.Optional[str]]]
        ] = []

    def registerMessageFilter(
        self, message_filters: tuple[str, ...], wrapped_function: typing.Callable
    ) -> None:
        """
        Registers a filter with a function

        :param `message_filters` message filters
        :param `wrapped_function` function to be executed on match
        """
        self.message_filters.append({message_filters: wrapped_function})

    def registerCallbackHandler(
        self, context: str, function: typing.Callable, value: typing.Optional[str] = ""
    ) -> None:
        self.callback_filters.append(
            {"context": context, "value": value, "callable": function}
        )

    def registerEditedMessageFilter(
        self, message_filters: tuple[str, ...], wrapped_function: typing.Callable
    ) -> None:
        """
        Registers a filter with a function

        :param `message_filters` message filters
        :param `wrapped_function` function to be executed on match
        """
        self.edited_message_filters.append({message_filters: wrapped_function})

    def registerDeleteddMessageFilter(self, wrapped_function: typing.Callable) -> None:
        """
        Registers a filter with a function

        :param `message_filters` message filters
        :param `wrapped_function` function to be executed on match
        """
        self.deleted_message_filters.append(wrapped_function)
