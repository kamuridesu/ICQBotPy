import typing

from ICQBot import ICQBot
from rawApiEventsMapperFunctions import getEvents
from exceptions.DispatcherErrors import *
from Message import ReceivedMessage

class Dispatcher:
    def __init__(self, bot_instance: ICQBot) -> None:
        if not isinstance(bot_instance, ICQBot): raise TypeError(f"Argument bot_instance must be Bot, not {type(bot_instance).__name__}!")
        self._bot_instance = bot_instance
        self._is_polling = False
        self._last_event_id = 0

    def _pollingHandler(self, response: dict[typing.Any, typing.Any]):
        print(response)
        print("----------", self._last_event_id)
        if response is not None:
            if response['events']:
                self._last_event_id = response['events'][-1]['eventId']
                last_event_type = response['events'][-1]['type']
                if last_event_type == "newMessage":
                    rc = (ReceivedMessage(response['events'][-1], self._bot_instance))
                    print(rc)
                    rc.reply("test")
    
    def start_polling(self, timeout: int=20) -> None:
        if self._is_polling:
            raise AlreadyPollingError

        self._is_polling = True

        while self._is_polling:
            try:
                self._pollingHandler(getEvents(self._bot_instance.token, self._bot_instance.endpoint, self._last_event_id, timeout))
            except KeyboardInterrupt:
                self._stopPolling()

    def registerMessageHandler(self, filter: typing.Union[str, list[str]], function: typing.Callable):
        def wrapper():
            function()
        

    def _stopPolling(self) -> None:
        self._is_polling = False


if __name__ == "__main__":
    bot = ICQBot("001.3476360037.4211413661:1004298326")
    dp = Dispatcher(bot)
    dp.start_polling()
