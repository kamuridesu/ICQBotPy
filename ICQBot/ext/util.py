import typing
import aiohttp
import json
import logging

from ..exceptions.ClientErrors import ClientError
from ..exceptions.ServerErrors import ServerError


def initLogger():
    logging.basicConfig(
        format="[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
        datefmt="%m-%d %H:%M:%S",
        filename="ICQBot.log",
        level=logging.DEBUG,
    )
    logger = logging.getLogger("icq")
    return logger


class CustomDict(dict):
    logger = initLogger()

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        if hasattr(self, "bot_instance"):
            x = self.copy()
            del x["bot_instance"]
            return repr(x)
        else:
            return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)


class Response(CustomDict):
    def __init__(self, status_code, content):
        self.status = status_code
        self.content = content

    async def json(self):
        return json.loads(self.content.decode("utf-8"))


async def sendGetRequest(session: aiohttp.ClientSession, *args, **kwargs) -> Response:
    """
    Function to send a rest request and return the Response
    :session A client session object from aiohttp
    :param *args and *kwargs to be used on the request
    :return a Response object with the content of the endpoint
    """
    response: typing.Union[Response, None] = None
    async with session.request("GET", *args, **kwargs) as resp:
        response = Response(resp.status, await resp.read())
        if response.status in range(400, 499):
            raise ClientError
        if response.status in range(500, 599):
            raise ServerError
    return response


async def sendPostRequest(session: aiohttp.ClientSession, *args, **kwargs) -> Response:
    """
    Function to send a rest request and return the Response
    :session A client session object from aiohttp
    :param *args and *kwargs to be used on the request
    :return a Response object with the content of the endpoint
    """
    response: typing.Union[Response, None] = None
    async with session.request("POST", *args, **kwargs) as resp:
        response = Response(resp.status, await resp.read())
        if response.status in range(400, 499):
            raise ClientError
        if response.status in range(500, 599):
            raise ServerError
    return response
