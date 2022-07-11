import typing
import requests

from ..exceptions.ClientErrors import ClientError
from ..exceptions.GenericErrors import NotExpectedError
from ..exceptions.ServerErrors import ServerError


def fetcher(get_post: str="get", *args, **kwargs) -> requests.Response:
    response: typing.Union[requests.Response, None] = None
    if get_post == "get":
        response = requests.get(*args, **kwargs)
    elif get_post == "post":
        response = requests.post(*args, **kwargs)
    else:
        raise NotExpectedError
    if response.status_code in range(500, 599):
        raise ServerError
    if response.status_code in range(400, 499):
        raise ClientError
    return response