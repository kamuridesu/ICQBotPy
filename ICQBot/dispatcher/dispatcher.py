import typing
import asyncio

from ..ICQBot import ICQBot
from ..mapper.EventsMapper import getEvents
from ..exceptions.DispatcherErrors import *
from ..messages.message import ReceivedMessage
from ..messages.callback import Callback
from .handlers import MessageHandlers, CallbackHandlers
from .filters import FiltersRegistry


class Dispatcher:
    """
    Dispatcher to process and handles with events
    """
    def __init__(self, bot_instance: ICQBot) -> None:
        if not isinstance(bot_instance, ICQBot): raise TypeError(f"Argument bot_instance must be Bot, not {type(bot_instance).__name__}!")
        self._bot_instance = bot_instance
        self._is_polling = False
        self._last_event_id = 0
        self.filterRegistry = FiltersRegistry()
        self.messageHandlers = MessageHandlers(self.filterRegistry)
        self.callbackHandlers = CallbackHandlers(self.filterRegistry)
        self.running_tasks = set()

    async def _pollingHandler(self, response: dict[typing.Any, typing.Any]):
        last_event_type = response['events'][-1]['type']
        if last_event_type == "newMessage":
            rc = (ReceivedMessage(response['events'][-1]['payload'], self._bot_instance))
            return await asyncio.gather(self.messageHandlers.handle(rc))
        if last_event_type == "callbackQuery":
            cb = Callback(response['events'][-1]['payload'], self._bot_instance)
            return await asyncio.gather(self.callbackHandlers.handle(cb))

    async def start_polling(self, timeout: int=20) -> None:
        """
        Start long-polling
        :param timeout:
        """
        if self._is_polling:
            raise AlreadyPollingError

        self._is_polling = True
        print("Polling started")

        while self._is_polling:
            try:
                updates = await getEvents(self._bot_instance.token, self._bot_instance.endpoint, self._last_event_id, timeout)
                if updates['events']:
                    self._last_event_id = updates['events'][-1]['eventId']
                    task = asyncio.create_task(self._pollingHandler(updates))
                    self.running_tasks.add(task)
                    task.add_done_callback(lambda t: self.running_tasks.remove(t))
            except KeyboardInterrupt:
                self._stopPolling()

    def message_handler(self, commands: typing.Union[str, list[str]]=""):
        """
        Decorator for message handler

        Examples:

        Simple commands handler:

            @dp.message_handler(commands=['start', 'welcome', 'about'])

            def cmd_handler(message: ReceivedMessage):
        

        :param `commands`: list of commands
        :return: decorated function
        """
        def decorator(function: typing.Callable):
            self.messageHandlers.register(commands, function)
            return function
        return decorator

    def callback_query_handler(self, context: str, value: typing.Any = ""):
        """
        Decorator for message handler

        Examples:

        Simple callback handler:

            @dp.callback_query_handler(context="callbackData")
            def callback_handler(callback: Callback):
        
        Callback handler to trigger when a specified value is used

            @dp.callback_query_handler(context="callbackData", value="hello")
            def callback_handler(callback: Callback):

        :param `commands`: list of commands
        :return: decorated function
        """
        def decorator(function: typing.Callable):
            self.callbackHandlers.register(context, function, str(value))
            return function
        return decorator

    def _stopPolling(self) -> None:
        self._is_polling = False


if __name__ == "__main__":
    ...
