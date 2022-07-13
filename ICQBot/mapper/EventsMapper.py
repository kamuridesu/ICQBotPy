import aiohttp
import typing

from ICQBot.exceptions.GenericErrors import NotExpectedError

from ..ext.util import fetcher, Response



async def getEvents(token: str, endpoint: str, last_event_id: int=0, poll_time: int=20) -> dict[typing.Any, typing.Any]:
    """
    Get events sent by the server

    params:
    - token: bot token
    - endpoint: api endpoint
    - last_event_id: last known event id
    - poll_time: pool_time

    return:
    - dict with the contents of the event
    """
    route = "/events/get?"
    query = f"token={token}&lastEventId={last_event_id}&pollTime={poll_time}"
    response: Response = await fetcher("get", endpoint + route + query)
    if response.status == 200:
        return (await response.json())
    raise NotExpectedError


if __name__ == "__main__":
    ...