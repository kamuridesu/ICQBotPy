import requests
from .ext.rawApiMessagesMapperFunctions import *
from .ext.rawApiChatMapperFunctions import *
from .ext.Message import SentMessage
from .exceptions.ClientErrors import InvalidTokenError


class ICQBot:
    def __init__(self, token: str) -> None:
        self.endpoint: str = "https://api.icq.net/bot/v1"
        self.token: str = token
        if verifyToken(self.token, self.endpoint) is False:
            raise InvalidTokenError
        
    def info(self) -> dict[str, typing.Any]:
        return getBotInfo(self.token, self.endpoint)

    def sendText(self, chat_id: str, text: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> SentMessage:
        return SentMessage(sendText(self.token, self.endpoint, chat_id, text, reply_message_id, forward_chat_id, forward_message_id, inline_keyboard_markup, formatting, parse_mode), self.token, self.endpoint)

    def editMessage(self, chat_id: str, message_id: str, text: str, inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> SentMessage:
        return editMessage(self.token, self.endpoint, chat_id, message_id, text, inline_keyboard_markup, formatting, parse_mode)

    def sendFile(self, chat_id: str, file: typing.Union[str, bytes, None]=None, file_id: str="", caption: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> dict[str, str]:
        return sendFile(self.token, self.endpoint, chat_id, file, file_id, caption, reply_message_id, forward_chat_id, forward_message_id, inline_keyboard_markup, formatting, parse_mode)

    def getFileInfo(self, file_id: str) -> dict[str, typing.Any]:
        return getFileInfo(self.token, self.endpoint, file_id)

    def downloadFile(self, file_id: str) -> bytes:
        response: requests.Response = requests.get(self.getFileInfo(file_id)['url'])
        if response.status_code == 200:
            return response.content
        raise FileNotFoundError

    def sendVoice(self, chat_id: str, file: typing.Union[str, bytes, None]=None, file_id: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup()) -> dict[str, typing.Any]:
        return sendVoice(self.token, self.endpoint, chat_id, file, file_id, reply_message_id, forward_chat_id, forward_message_id, inline_keyboard_markup)

    def removeMembers(self, chat_id: str, members: typing.Union[list[typing.Union[str, int]], str, int]) -> bool:
        members_dict: list[dict[str, typing.Union[str, int]]] = []
        if isinstance(members, list):
            for member in members:
                members_dict.append({
                    "sn": str(member)
                })
        elif isinstance(members, str):
            members_dict.append({"sn": members})
        else:
            raise TypeError("Invalid user!")
        return removeMembers(self.token, self.endpoint, chat_id, members_dict)


if __name__ == "__main__":
    ...
