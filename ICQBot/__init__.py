from .dispatcher import Dispatcher
from .ICQBot import ICQBot
import asyncio
from .exceptions.GenericErrors import NotExpectedError
from .ext.util import initLogger


def executor(dp: Dispatcher, poll_time: int = 20):
    logger = initLogger()
    if not isinstance(dp, Dispatcher):
        err_msg: str = f"Expected a Dispatcher, got {type(dp).__name__}"
        logger.error(err_msg)
        raise NotExpectedError(err_msg)
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(dp.start_polling(poll_time))
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.warn("Exiting...")
        pass
    finally:
        loop.run_until_complete(dp._stopPolling())


__all__ = ["Dispatcher", "ICQBot", "executor"]
