import typing

from ..messages.message import ReceivedMessage
from ..messages.callback import Callback
from .filters import FiltersRegistry


class MessageHandlers:
    """
    Handles filter registration and matches
    """

    def __init__(self, filtersRegister: FiltersRegistry) -> None:
        self.filtersRegister = filtersRegister

    def register(
        self, message_filters: typing.Union[str, list[str]], function: typing.Callable
    ) -> None:
        """
        Register a filter to the filters registry

        :param `message_filters` message filters
        :param `functoin` function to be executed on match
        """
        filters: list[str] = []
        if isinstance(message_filters, list):
            filters = message_filters
        elif isinstance(message_filters, str):
            filters.append(message_filters)
        return self.filtersRegister.registerMessageFilter(tuple(filters), function)

    async def handle(self, message: ReceivedMessage):
        """
        Handles a `ReceivedMessage` event and if it matches a filter, it executes the assigned function
        :param `message` the received message
        """
        global_catcher: typing.Union[typing.Callable, None] = None
        for _filter in self.filtersRegister.message_filters:
            for filters, function in _filter.items():
                for f in filters:
                    if message.text.startswith(f) and f != "":
                        return await function(message)
                    elif f == "":
                        global_catcher = function
        if global_catcher is not None:
            await global_catcher(message)


class CallbackHandlers(MessageHandlers):
    def register(self, context: str, function=typing.Callable, value: typing.Optional[str] = "") -> None:  # type: ignore
        """
        Register a filter to the filters registry

        :param `context`: Callback context (key)
        :param `function` function to be executed on match
        :param `value`: value to be matched (optional)
        """
        self.filtersRegister.registerCallbackHandler(context, function, value)

    async def handle(self, callback: Callback):  # type: ignore
        """
        Handles a callback query event and if it matches a filter, it executes the assigned function
        : param `callback`: the callback query
        """
        func: typing.Union[typing.Callable, None] = None
        for _filter in self.filtersRegister.callback_filters:
            if (
                _filter["context"] in callback
                and callback[_filter["context"]] == _filter["value"]
            ):
                if (
                    not isinstance(_filter["callable"], str)
                    and _filter["callable"] is not None
                ):
                    func = _filter["callable"]
            elif _filter["context"] in callback and _filter["value"] == "":
                if (
                    not isinstance(_filter["callable"], str)
                    and _filter["callable"] is not None
                ):
                    func = _filter["callable"]
            if func is not None:
                return await func(callback)


class EditedMessageHandlers(MessageHandlers):
    """
    Handles filter registration and matches
    """

    def register(
        self, message_filters: typing.Union[str, list[str]], function: typing.Callable
    ) -> None:
        """
        Register a filter to the filters registry

        :param `message_filters` message filters
        :param `functoin` function to be executed on match
        """
        filters: list[str] = []
        if isinstance(message_filters, list):
            filters = message_filters
        elif isinstance(message_filters, str):
            filters.append(message_filters)
        return self.filtersRegister.registerEditedMessageFilter(
            tuple(filters), function
        )

    async def handle(self, message: ReceivedMessage):
        """
        Handles a `ReceivedMessage` event and if it matches a filter, it executes the assigned function
        :param `message` the received message
        """
        for _filter in self.filtersRegister.edited_message_filters:
            for filters, function in _filter.items():
                for f in filters:
                    if message.text.startswith(f):
                        return await function(message)


class DeletedMessageHandlers(MessageHandlers):
    """
    Handles filter registration and matches
    """

    def register(self, function: typing.Callable) -> None:
        """
        Register a filter to the filters registry

        :param `message_filters` message filters
        :param `functoin` function to be executed on match
        """
        return self.filtersRegister.registerDeletedMessageFilter(function)

    async def handle(self, message: ReceivedMessage):
        """
        Handles a `ReceivedMessage` event and if it matches a filter, it executes the assigned function
        :param `message` the received message
        """
        for func in self.filtersRegister.deleted_message_filters:
            return await func(message)


class PinnedMessageHandlers(MessageHandlers):
    """
    Handles filter registration and matches
    """

    def register(self, function: typing.Callable) -> None:
        """
        Register a filter to the filters registry

        :param `message_filters` message filters
        :param `functoin` function to be executed on match
        """
        return self.filtersRegister.registerPinnedMessageFilter(function)

    async def handle(self, message: ReceivedMessage):
        """
        Handles a `ReceivedMessage` event and if it matches a filter, it executes the assigned function
        :param `message` the received message
        """
        for func in self.filtersRegister.pinned_message_filters:
            return await func(message)


if __name__ == "__main__":
    ...
