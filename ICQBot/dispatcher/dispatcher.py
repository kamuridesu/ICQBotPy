import typing
import aiohttp
import asyncio

from ..ICQBot import ICQBot
from ..mapper.EventsMapper import getEvents
from ..exceptions.DispatcherErrors import AlreadyPollingError
from ..messages.message import DeletedMessage, ReceivedMessage, PinnedMessage
from ..messages.callback import Callback
from .handlers import (
    DeletedMessageHandlers,
    EditedMessageHandlers,
    PinnedMessageHandlers,
    MessageHandlers,
    CallbackHandlers,
)
from .filters import FiltersRegistry


class Dispatcher:
    """
    Dispatcher to process and handles with events
    """

    def __init__(self, bot_instance: ICQBot) -> None:
        if not isinstance(bot_instance, ICQBot):
            err_msg: str = (
                f"Argument bot_instance must be Bot, not {type(bot_instance).__name__}!"
            )
            self.logger.error(err_msg)
            raise TypeError(err_msg)
        self._bot_instance = bot_instance
        self._session = aiohttp.ClientSession()
        self._bot_instance.setClientSession(self._session)
        self._is_polling = False
        self._last_event_id = 0
        self.filterRegistry = FiltersRegistry()
        self.messageHandlers = MessageHandlers(self.filterRegistry)
        self.callbackHandlers = CallbackHandlers(self.filterRegistry)
        self.editedMessageHandlers = EditedMessageHandlers(self.filterRegistry)
        self.deletedMessageHandlers = DeletedMessageHandlers(self.filterRegistry)
        self.pinnedMessageHandlers = PinnedMessageHandlers(self.filterRegistry)
        self.running_tasks: set[asyncio.Task] = set()

    async def _pollingHandler(self, response: dict[typing.Any, typing.Any]):
        last_event_type = response["events"][-1]["type"]
        if last_event_type == "newMessage":
            rc = ReceivedMessage(response["events"][-1]["payload"], self._bot_instance)
            return await asyncio.gather(self.messageHandlers.handle(rc))
        if last_event_type == "callbackQuery":
            cb = Callback(response["events"][-1]["payload"], self._bot_instance)
            return await asyncio.gather(self.callbackHandlers.handle(cb))
        if last_event_type == "editedMessage":
            em = ReceivedMessage(response["events"][-1]["payload"], self._bot_instance)
            return await asyncio.gather(self.editedMessageHandlers.handle(em))
        if last_event_type == "deletedMessage":
            dm = DeletedMessage(response["events"][-1]["payload"])
            return await asyncio.gather(self.deletedMessageHandlers.handle(dm))
        if last_event_type in ["pinnedMessage", "unpinnedMessage"]:
            pinned = True if last_event_type == "pinnedMessage" else False
            pm = PinnedMessage(
                response["events"][-1]["payload"], self._bot_instance, pinned
            )
            return await asyncio.gather(self.pinnedMessageHandlers.handle(pm))

    async def start_polling(self, pool_time: int = 20) -> None:
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
                updates = await getEvents(
                    self._bot_instance.session,
                    self._bot_instance.token,
                    self._bot_instance.endpoint,
                    self._last_event_id,
                    pool_time,
                )
                if updates["events"]:
                    self._last_event_id = updates["events"][-1]["eventId"]
                    task = asyncio.create_task(self._pollingHandler(updates))
                    self.running_tasks.add(task)
                    task.add_done_callback(lambda t: self.running_tasks.remove(t))
            except KeyboardInterrupt:
                await self._stopPolling()

    def message_handler(self, commands: typing.Union[str, list[str]] = ""):
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

    def edited_message_handler(self, commands: typing.Union[str, list[str]] = ""):
        """
        Decorator for message handler

        Examples:

        Simple callback handler:

            @dp.edited_message_handler(commands=['start', 'welcome', 'about'])

            def cmd_handler(message: ReceivedMessage):


        :param `commands`: list of commands
        :return: decorated function
        """

        def decorator(function: typing.Callable):
            self.editedMessageHandlers.register(commands, function)
            return function

        return decorator

    def pinned_message_handler(self):
        """
        Decorator for message handler

        Examples:

        Simple callback handler:

            @dp.pinned_message_handler(commands=['start', 'welcome', 'about'])

            def cmd_handler(message: ReceivedMessage):


        :param `commands`: list of commands
        :return: decorated function
        """

        def decorator(function: typing.Callable):
            self.pinnedMessageHandlers.register(function)
            return function

        return decorator

    def deleted_message_handler(self):
        """
        Decorator for message handler

        Examples:

        Simple callback handler:

            @dp.deleted_message_handler(commands=['start', 'welcome', 'about'])

            def cmd_handler(message: ReceivedMessage):


        :param `commands`: list of commands
        :return: decorated function
        """

        def decorator(function: typing.Callable):
            self.deletedMessageHandlers.register(function)
            return function

        return decorator

    async def _stopPolling(self) -> None:
        self._is_polling = False
        [t.cancel() for t in self.running_tasks]
        self.running_tasks = set()

    async def __aenter__(self):
        self.logger.debug("Entering context")
        await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, tb):
        if self.session:
            self.logger.debug("Exit context")
            await self.session.__aexit__(exc_type, exc_val, tb)

    async def close(self):
        if self.session:
            await self.session.close()


if __name__ == "__main__":
    ...
