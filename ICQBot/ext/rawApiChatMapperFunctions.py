
from aiohttp import ServerDisconnectedError
import requests
import typing
import os
import json

try:
    from exceptions.ClientErrors import ClientError
    from exceptions.GenericErrors import NotExpectedError
    from exceptions.GroupErrors import *
    from parseModes import *
    from Keyboards import *
except ImportError:
    from ..exceptions.ClientErrors import ClientError
    from ..exceptions.GenericErrors import NotExpectedError
    from ..exceptions.GroupErrors import *
    from .parseModes import *
    from .Keyboards import *


def fetcher(get_post: str="get", *args, **kwargs) -> requests.Response:
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


def removeMembers(token: str, endpoint: str, chat_id: str, members: list[dict]) -> bool:
    route = "/chats/members/delete?"
    query = f"token={token}&chatId={chat_id}&members={json.dumps(members)}"
    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code in range(200, 299):
        return response.json()['ok']
    raise CannotRemoveUsersError


if __name__ == "__main__":
    ...