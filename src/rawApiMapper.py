
from aiohttp import ServerDisconnectedError
import requests
import typing
import os
import json

try:
    from exceptions.ClientErrors import ClientError
    from exceptions.GenericErrors import NotExpectedError
    from exceptions.MessageErrors import *

    from parseModes import *
    from Keyboards import *
    from Message import *
except ImportError:
    from .exceptions.ClientErrors import ClientError
    from .exceptions.GenericErrors import NotExpectedError
    from .exceptions.MessageErrors import *

    from .parseModes import *
    from .Keyboards import *
    from .Message import *


def fetcher(*args, **kwargs) -> requests.Response:
    response: requests.Response = requests.get(*args, **kwargs)
    if response.status_code in range(500, 599):
        raise ServerDisconnectedError
    if response.status_code in range(400, 499):
        raise ClientError
    return response


class RawApiMapper:
    def __init__(self, token: str) -> None:
        self.endpoint: str = "https://api.icq.net/bot/v1"
        self.token: str = token

    def verifyToken(self) -> bool:
        info: dict[str, typing.Any] = self.getSelfInfo()
        return info['ok']

    def getSelfInfo(self) -> dict[str, typing.Any]:
        response: requests.Response = fetcher(self.endpoint + "/self/get?token=" + self.token)

        if response and response.status_code == 200:
            return response.json()
        raise NotExpectedError("Server response is empty or invalid!")

    def sendText(self, chat_id: str, text: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> dict[str, str]:
        route = "/messages/sendText?"
        query = f"token={self.token}&chatId={chat_id}"
        if text:
            query += f"&text={text}"
        if reply_message_id:
            query += f"&replyMsgId={reply_message_id}"
        if forward_chat_id:
            query += f"&forwardChatId={forward_chat_id}"
        if forward_message_id:
            query += f"&forwardMsgId={forward_message_id}"
        if inline_keyboard_markup.getButtonsAsString():
            query += f"&inlineKeyboardMarkup={inline_keyboard_markup.getButtonsAsString()}"
        if formatting.content:
            query += f"&format={formatting.content}"
        if parse_mode:
            query += f"&parseMode={parse_mode.content}"
        response: requests.Response = requests.get(self.endpoint + route + query)
        if response.status_code in range(200, 299):
            response_dict: dict = response.json()
            if response_dict['ok']:
                return Message(response_dict)
            else:
                raise MessageNotSentError(response_dict['description'])
        raise MessageNotSentError


    def sendFile(self, chat_id: str, file: typing.Union[str, bytes, None]=None, file_id: str="", caption: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> dict[str, str]:
        route = "/messages/sendFile?"
        query = f"token={self.token}&chatId={chat_id}"
        response: typing.Union[requests.Response, None] = None
        if file_id and file:
            raise AmbigousFileError
        if caption:
            query += f"&caption={caption}"
        if reply_message_id:
            query += f"&replyMsgId={reply_message_id}"
        if forward_chat_id:
            query += f"&forwardChatId={forward_chat_id}"
        if forward_message_id:
            query += f"&forwardMsgId={forward_message_id}"
        if inline_keyboard_markup.getButtonsAsString():
            query += f"&inlineKeyboardMarkup={inline_keyboard_markup.getButtonsAsString()}"
        if formatting.content:
            query += f"&format={formatting.content}"
        if parse_mode:
            query += f"&parseMode={parse_mode.content}"
        if file_id:
            query += f"&fileId={file_id}"
            response = requests.get(self.endpoint + route + query)
        elif file:
            content: typing.Union[dict[str, bytes], None] = None
            if isinstance(file, bytes):
                content = {'file': ('noname', file)}
            elif isinstance(file, str):
                if not os.path.isfile(file):
                    raise FileNotFoundError
                with open(file, "rb") as file_bytes:
                    content = {'file': ('noname', file_bytes.read())}
            if content is None:
                raise FileTypeMismatchError
            response = requests.post(self.endpoint + route + query, files=content)
        
        if response is None:
            raise NotExpectedError("File cannot be uploaded! Cause unknown")
            
        if response.status_code in range(200, 299):
            response_dict: dict = response.json()
            if response_dict['ok']:
                return response_dict
            else:
                raise MessageNotSentError(response_dict['description'])
        raise MessageNotSentError



if __name__ == "__main__":
    api_mapper = RawApiMapper("001.1917418351.1245850609:1004146438")
    # print(api_mapper.verifyToken())
    # api_mapper.sendText("@kamuridesu", "heloo gugulu")
    api_mapper.sendFile("@kamuridesu", file_id="0847P000fn3659v0PqH5NT62b5e5ef1ah", caption="repost")

    # print(api_mapper.getSelfInfo())
