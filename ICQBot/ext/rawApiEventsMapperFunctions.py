from aiohttp import ServerDisconnectedError
import requests
import typing
import os

try:
    from exceptions.ClientErrors import ClientError
    from exceptions.GenericErrors import NotExpectedError
    from exceptions.MessageErrors import *

    from parseModes import *
    from Keyboards import *
except ImportError:
    from ..exceptions.ClientErrors import ClientError
    from ..exceptions.GenericErrors import NotExpectedError
    from ..exceptions.MessageErrors import *

    from .parseModes import *
    from .Keyboards import *


def fetcher(get_post: str="get", *args, **kwargs) -> requests.Response:
    """
    Fetches the content of a url, receives same arguments as `requests.post` and `requests.get`

    params:
    - get_post:

    returns:
    - requests.Response: The content of the url
    """
    response: typing.Union[requests.Response, None] = None
    if get_post == "get":
        response = requests.get(*args, **kwargs)
    elif get_post == "post":
        response = requests.post(*args, **kwargs)
    else:
        raise NotExpectedError
    if response.status_code in range(500, 599):
        raise ServerDisconnectedError
    if response.status_code in range(400, 499):
        raise ClientError
    return response


def getEvents(token: str, endpoint: str, last_event_id: int=0, poll_time: int=20) -> dict[typing.Any, typing.Any]:
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
    response: requests.Response = fetcher("get", endpoint + route + query)
    if response.status_code == 200:
        return response.json()


if __name__ == "__main__":
    ...