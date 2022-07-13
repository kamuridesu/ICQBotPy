import typing
from copy import deepcopy
import aiohttp
import json

from ..exceptions.ClientErrors import ClientError
from ..exceptions.GenericErrors import NotExpectedError
from ..exceptions.ServerErrors import ServerError


class CustomDict(dict):
    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        if hasattr(self, "bot_instance"):
            x = deepcopy(self)
            del x['bot_instance']
            return repr(x.__dict__)
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


async def fetcher(get_post: str="get", *args, **kwargs):
    """
    function to fetch data from endpoints
    :param get_post: REST option (defaults to get)
    :param *args and *kwargs to be used by session
    :return a Response object with the content of the endpoint
    """
    response: typing.Union[Response, None] = None
    async with aiohttp.ClientSession() as session:
        if get_post == "get":
            async with session.get(*args, **kwargs) as _response:
                response = Response(_response.status, await _response.read())
        elif get_post == "post":
            async with session.post(*args, **kwargs) as _response:
                response = Response(_response.status, await _response.read())
        else:
            raise NotExpectedError
        if response.status in range(500, 599):
            raise ServerError
        if response.status in range(400, 499):
            raise ClientError
    return response

