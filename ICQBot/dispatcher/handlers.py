import typing

from ..messages.message import ReceivedMessage
from .filters import FiltersRegistry



class MessageHandlers:
    def __init__(self, filtersRegister: FiltersRegistry) -> None:
        self.filtersRegister = filtersRegister

    def register(self, message_filters: typing.Union[str, list[str]], function: typing.Callable) -> None:
        filters: list[str] = []
        if isinstance(message_filters, list):
            filters = (message_filters)
        elif isinstance(message_filters, str):
            filters.append(message_filters)
        return self.filtersRegister.register(tuple(filters), function)

    def handle(self, message: ReceivedMessage):
        for _filter in self.filtersRegister.filters:
            for filters, function in _filter.items():
                for f in filters:
                    if message.text.startswith(f):
                        return function(message)


if __name__ == "__main__":
    ...