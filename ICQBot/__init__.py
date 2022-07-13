from .dispatcher import Dispatcher
from .ICQBot import ICQBot
import asyncio
from .exceptions.GenericErrors import NotExpectedError


def executor(dp: Dispatcher):
    if not isinstance(dp, Dispatcher):
        raise NotExpectedError(f"Expected a Dispatcher, got {type(dp).__name__}")
    try:
        asyncio.run(dp.start_polling())
    except KeyboardInterrupt:
        dp._stopPolling()
    


__all__ = ["Dispatcher", "ICQBot", "executor"]
