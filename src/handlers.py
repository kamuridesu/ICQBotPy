import typing
from Message import ReceivedMessage
from filters import FiltersRegistry


class MessageHandlersFactory:
    def __init__(self, message_filter: typing.Union[str, list[str]], function: typing.Callable, filtersRegister: FiltersRegistry) -> None:
        # self.bot_instance = bot_instance
        self.function_to_be_wrapped = function
        self.message_filter = []
        if isinstance(message_filter, list):
            self.message_filter = message_filter
        else:
            self.message_filter.append(message_filter)
        self.filter_registry_instance = filtersRegister

    def register(self):
        self.filter_registry_instance.register(tuple(self.message_filter), self.function_to_be_wrapped)


class MessageHandler:
    def __init__(self, filtersRegister: FiltersRegistry, message: ReceivedMessage) -> None:
        for _filter in filtersRegister.filters:
            for filters, function in _filter.items():
                for f in filters:
                    if message.text.startswith(f):
                        return function(message)


if __name__ == "__main__":
    ...