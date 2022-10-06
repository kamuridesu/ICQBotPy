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

    async def handle(self, message: ReceivedMessage):
        """
        Handles a `ReceivedMessage` event and if it matches a filter, it executes the assigned function
        :param `message` the received message
        """
        for _filter in self.filtersRegister.message_filters:
            for filters, function in _filter.items():
                for f in filters:
                    if message.text.startswith(f):
                        return await function(message)


class CallbackHandlers(MessageHandlers):
    def register(self, context: str, function=typing.Callable, value: typing.Optional[str]="") -> None: # type: ignore
        """
        Register a filter to the filters registry

        :param `context`: Callback context (key)
        :param `function` function to be executed on match
        :param `value`: value to be matched (optional)
        """
        self.filtersRegister.registerCallbackHandler(context, function, value)

    async def handle(self, callback: Callback): # type: ignore
        """
        Handles a callback query event and if it matches a filter, it executes the assigned function
        : param `callback`: the callback query
        """
        func: typing.Union[typing.Callable, None] = None
        for _filter in self.filtersRegister.callback_filters:
            if _filter['context'] in callback and callback[_filter['context']] == _filter['value']:
                if not isinstance(_filter['callable'], str) and _filter['callable'] is not None:
                    func = _filter['callable']
            elif _filter['context'] in callback and _filter["value"] == "":
                if not isinstance(_filter['callable'], str) and _filter['callable'] is not None:
                    func = _filter['callable']
            if func is not None:
                return func(callback)
            


if __name__ == "__main__":
    ...