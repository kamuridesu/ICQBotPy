
import requests
import json

from ..exceptions.GroupErrors import *
from ..ext.parseModes import *
from ..ext.Keyboards import *
from ..ext.util import fetcher



def removeMembers(token: str, endpoint: str, chat_id: str, members: list[dict]) -> bool:
    route = "/chats/members/delete?"
    query = f"token={token}&chatId={chat_id}&members={json.dumps(members)}"
    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise CannotRemoveUsersError


if __name__ == "__main__":
    ...