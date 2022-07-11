
import requests
import json

from ..exceptions.GroupErrors import *
from ..exceptions.GenericErrors import NotExpectedError
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


def getChatInfo(token: str, endpoint: str, chat_id: str) -> dict:
    route = "/chats/getInfo?"
    query = f"token={token}&chatId={chat_id}"
    response: requests.Response = fetcher("get", endpoint + route + query)
    if response.status_code == 200:
        if "ok" in response.json() and response.json()['ok'] is False:
            raise GroupError(response.json()['description'])
        return response.json()
    raise NotExpectedError("Algo deu errado!")


def getChatAdmins(token: str, endpoint: str, chat_id: str) -> list[dict]:
    route = "/chats/getAdmins?"
    query = f"token={token}&chatId={chat_id}"
    response: requests.Response = fetcher("get", endpoint + route + query)
    if response.status_code == 200:
        if "ok" in response.json() and response.json()['ok'] is False:
            raise GroupError(response.json()['description'])
        return response.json()['admins']
    raise NotExpectedError("Algo deu errado!")


def getChatMembers(token: str, endpoint: str, chat_id: str) -> list[dict]:
    # needs to impl cursor
    route = "/chats/getMembers?"
    query = f"token={token}&chatId={chat_id}"
    response: requests.Response = fetcher("get", endpoint + route + query)
    if response.status_code == 200:
        if "ok" in response.json() and response.json()['ok'] is False:
            raise GroupError(response.json()['description'])
        return response.json()['members']
    raise NotExpectedError("Algo deu errado!")


def getChatBlockedUsers(token: str, endpoint: str, chat_id: str) -> list[dict]:
    route = "/chats/getBlockedUsers?"
    query = f"token={token}&chatId={chat_id}"
    response: requests.Response = fetcher("get", endpoint + route + query)
    if response.status_code == 200:
        if "ok" in response.json() and response.json()['ok'] is False:
            raise GroupError(response.json()['description'])
        return response.json()['users']
    raise NotExpectedError("Algo deu errado!")


def getPendingMembers(token: str, endpoint: str, chat_id: str) -> list[dict]:
    route = "/chats/getPendingUsers?"
    query = f"token={token}&chatId={chat_id}"
    response: requests.Response = fetcher("get", endpoint + route + query)
    if response.status_code == 200:
        if "ok" in response.json() and response.json()['ok'] is False:
            raise GroupError(response.json()['description'])
        return response.json()['users']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


def blockChatUser(token: str, endpoint: str, chat_id: str, user_id: str, delete_last_messages: bool=False) -> bool:
    route = "/chats/blockUser?"
    query = f"token={token}&chatId={chat_id}&userId={user_id}&delLastMessages={json.dumps(delete_last_messages)}"
    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


def unblockChatUser(token: str, endpoint: str, chat_id: str, user_id: str) -> bool:
    route = "/chats/unblockUser?"
    query = f"token={token}&chatId={chat_id}&userId={user_id}"
    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


def resolvePendingUsers(token: str, endpoint: str, chat_id: str, approve: bool, user_id: str="", everyone: bool=False) -> bool:
    route = "/chats/resolvePending?"
    query = f"token={token}&chatId={chat_id}&approve={json.dumps(approve)}"
    if everyone:
        query += f"&everyone={json.dumps(everyone)}"
    elif user_id != "":
        query += f"&userId={user_id}"
    
    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


def setGroupName(token: str, endpoint: str, chat_id: str, new_name: str) -> bool:
    route = "/chats/setTitle?"
    query = f"token={token}&chatId={chat_id}&title={new_name}"

    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


def setGroupAbout(token: str, endpoint: str, chat_id: str, about: str) -> bool:
    route = "/chats/setAbout?"
    query = f"token={token}&chatId={chat_id}&about={about}"

    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


def setGroupRules(token: str, endpoint: str, chat_id: str, rules: str) -> bool:
    route = "/chats/setRules?"
    query = f"token={token}&chatId={chat_id}&rules={rules}"

    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


def pinMessage(token: str, endpoint: str, chat_id: str, message_id: str) -> bool:
    route = "/chats/pinMessage?"
    query = f"token={token}&chatId={chat_id}&msgId={message_id}"

    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


def unpinMessage(token: str, endpoint: str, chat_id: str, message_id: str) -> bool:
    route = "/chats/unpinMessage?"
    query = f"token={token}&chatId={chat_id}&msgId={message_id}"

    response: requests.Response = fetcher("get", endpoint + route + query)

    if response.status_code == 200:
        return response.json()['ok']
    raise NotExpectedError("Algo deu errado! Verifique se o bot é admin!")


if __name__ == "__main__":
    ...