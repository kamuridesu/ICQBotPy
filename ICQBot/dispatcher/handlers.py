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

    def register(self, message_filters: typing.Union[str, list[str]], function: typing.Callable) -> None:
        """
        Register a filter to the filters registry

        :param `message_filters` message filters
        :param `functoin` function to be executed on match
        """
        filters: list[str] = []
        if isinstance(message_filters, list):
            filters = (message_filters)
        elif isinstance(message_filters, str):
            filters.append(message_filters)
        return self.filtersRegister.registerMessageFilter(tuple(filters), function)

    def handle(self, message: ReceivedMessage):
        """
        Handles a `ReceivedMessage` event and if it matches a filter, it executes the assigned function
        :param `message` the received message
        """
        for _filter in self.filtersRegister.message_filters:
            for filters, function in _filter.items():
                for f in filters:
                    if message.text.startswith(f):
                        return function(message)


class CallbackHandlers(MessageHandlers):
    def register(self, context: str, function=typing.Callable, value: typing.Optional[str]="") -> None:
        """
        Register a filter to the filters registry

        :param `context`: Callback context (key)
        :param `function` function to be executed on match
        :param `value`: value to be matched (optional)
        """
        self.filtersRegister.registerCallbackHandler(context, function, value)

    def handle(self, callback: Callback):
        """
        Handles a callback query event and if it matches a filter, it executes the assigned function
        : param `callback`: the callback query
        """
        for _filter in self.filtersRegister.callback_filters:
            if _filter['context'] in callback and callback[_filter['context']] == _filter['value']:
                return _filter['callable'](callback)
            elif _filter['context'] in callback and _filter["value"] == "":
                return _filter['callable'](callback)
            


if __name__ == "__main__":
    ...