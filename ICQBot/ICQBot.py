import requests
from .mapper.MessagesMapper import *
from .mapper.ChatMapper import *
from .messages.message import SentMessage
from .exceptions.ClientErrors import InvalidTokenError


class ICQBot:
    def __init__(self, token: str) -> None:
        self.endpoint: str = "https://api.icq.net/bot/v1"
        self.token: str = token
        if verifyToken(self.token, self.endpoint) is False:
            raise InvalidTokenError
        
    def info(self) -> dict[str, typing.Any]:
        """
        :return dict with information about the bot
        """
        return getBotInfo(self.token, self.endpoint)

    def sendText(self, chat_id: str, text: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> SentMessage:
        """
        Sends a text message
        :param chat_id: the id of the chat
        :param text: the content of the message
        :param reply_message_id: the id of a message to be replyed
        :param forward_chat_id: the if of the chat where the message can be forwarded
        :param inline_keyboard_markup: keyboard markup to use with callbacks
        :param formating: Formating of the message
        :param parse_mode: Parsing mode (Markdown or HTML)
        :return: SentMessage object with the data of the sent message
        """
        return SentMessage(sendText(self.token, self.endpoint, chat_id, text, reply_message_id, forward_chat_id, forward_message_id, inline_keyboard_markup, formatting, parse_mode), self)

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

    def getChatInfo(self, chat_id: str) -> dict:
        return getChatInfo(self.token, self.endpoint, chat_id)

    def getChatAdmins(self, chat_id: str) -> list[dict]:
        return getChatAdmins(self.token, self.endpoint, chat_id)
    
    def getChatMembers(self, chat_id: str) -> list[dict]:
        return getChatMembers(self.token, self.endpoint, chat_id)

    def getChatBlockedUsers(self, chat_id: str) -> list[dict]:
        return getChatBlockedUsers(self.token, self.endpoint, chat_id)

    def getPendingMembers(self, chat_id: str) -> list[dict]:
        return getPendingMembers(self.token, self.endpoint, chat_id)

    def blockChatUser(self, chat_id: str, user_id: str, delete_last_messages: bool=False) -> bool:
        return getPendingMembers(self.token, self.endpoint, chat_id, user_id, delete_last_messages)
    
    def unblockChatUser(self, chat_id: str, user_id: str) -> bool:
        return unblockChatUser(self.token, self.endpoint, chat_id, user_id)

    def resolvePendingUsers(self, chat_id: str, approve: bool, user_id: str="", everyone: bool=False) -> bool:
        return resolvePendingUsers(self.token, self.endpoint, chat_id, approve, user_id, everyone)
    
    def setGroupName(self, chat_id: str, new_name: str) -> bool:
        return setGroupName(self.token, self.endpoint, chat_id, new_name)

    def setGroupAbout(self, chat_id: str, about: str) -> bool:
        return setGroupAbout(self.token, self.endpoint, chat_id, about)

    def setGroupRules(self, chat_id: str, rules: str) -> bool:
        return setGroupRules(self.token, self.endpoint, chat_id, rules)

    def pinMessage(self, chat_id: str, message_id: str) -> bool:
        return pinMessage(self.token, self.endpoint, chat_id, message_id)

    def unpinMessage(self, chat_id: str, message_id: str) -> bool:
        return unpinMessage(self.token, self.endpoint, chat_id, message_id)


if __name__ == "__main__":
    ...
