from .dispatcher import Dispatcher
from .ICQBot import ICQBot
import asyncio
from .exceptions.GenericErrors import NotExpectedError


def loopExceptionHandler(loop, context):
    loop.default_exception_handler(context)

    exception = context.get("exception")
    if isinstance(exception, Exception):
        # loop.stop()
        pass


def executor(dp: Dispatcher, poll_time: int = 20):
    if not isinstance(dp, Dispatcher):
        err_msg: str = f"Expected a Dispatcher, got {type(dp).__name__}"
        raise NotExpectedError(err_msg)
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(loopExceptionHandler)
    try:
        loop.create_task(dp.start_polling(poll_time))
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(dp._stopPolling())


__all__ = ["Dispatcher", "ICQBot", "executor"]
