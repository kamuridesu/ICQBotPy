from .dispatcher import Dispatcher
from .ICQBot import ICQBot
import asyncio
from .exceptions.GenericErrors import NotExpectedError


def executor(dp: Dispatcher, timeout: int=20):
    if not isinstance(dp, Dispatcher):
        raise NotExpectedError(f"Expected a Dispatcher, got {type(dp).__name__}")
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(dp.start_polling(timeout))
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(dp._stopPolling())


__all__ = ["Dispatcher", "ICQBot", "executor"]
