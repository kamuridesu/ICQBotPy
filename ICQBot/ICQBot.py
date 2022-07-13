import asyncio

from .mapper.MessagesMapper import *
from .ext.util import fetcher, Response
from .mapper.ChatMapper import *
from .messages.message import SentMessage
from .exceptions.ClientErrors import InvalidTokenError


class ICQBot:
    def __init__(self, token: str) -> None:
        self.endpoint: str = "https://api.icq.net/bot/v1"
        self.token: str = token
        if asyncio.run(verifyToken(self.token, self.endpoint)) is False:
            raise InvalidTokenError
        
    async def info(self) -> dict[str, typing.Any]:
        """
        :return dict with information about the bot
        """
        return await getBotInfo(self.token, self.endpoint)

    async def sendText(self, chat_id: str, text: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting(), parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> SentMessage:
        """
        Sends a text message
        :param chat_id: the id of the chat
        :param text: the content of the message
        :param reply_message_id: the id of a message to be replyed
        :param forward_chat_id: the if of the chat where the message can be forwarded
        :param inline_keyboard_markup: keyboard markup to use with callbacks
        :param formatting: Formating of the message
        :param parse_mode: Parsing mode (Markdown or HTML)
        :return: SentMessage object with the data of the sent message
        """
        return SentMessage(await sendText(self.token, self.endpoint, chat_id, text, reply_message_id, forward_chat_id, forward_message_id, inline_keyboard_markup, formatting, parse_mode), self)

    async def editMessage(self, chat_id: str, message_id: str, text: str, inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting(), parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> dict[str, typing.Any]:
        """
        Edits a text message
        :param chat_id: the id of the chat
        :param text: the content of the message
        :param forward_chat_id: the if of the chat where the message can be forwarded
        :param inline_keyboard_markup: keyboard markup to use with callbacks
        :param formatting: Formating of the message
        :param parse_mode: Parsing mode (Markdown or HTML)
        :return: object with the data of the sent message
        """
        return await editMessage(self.token, self.endpoint, chat_id, message_id, text, inline_keyboard_markup, formatting, parse_mode)

    async def sendFile(self, chat_id: str, file: typing.Union[str, bytes, None]=None, file_id: str="", caption: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting(), parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> dict[str, str]:
        return await sendFile(self.token, self.endpoint, chat_id, file, file_id, caption, reply_message_id, forward_chat_id, forward_message_id, inline_keyboard_markup, formatting, parse_mode)

    async def getFileInfo(self, file_id: str) -> dict[str, typing.Any]:
        return await getFileInfo(self.token, self.endpoint, file_id)

    async def downloadFile(self, file_id: str) -> bytes:
        response: Response = await fetcher("get", (await self.getFileInfo(file_id))['url'])
        if response.status == 200:
            return response.content
        raise FileNotFoundError

    async def sendVoice(self, chat_id: str, file: typing.Union[str, bytes, None]=None, file_id: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup()) -> dict[str, typing.Any]:
        return await sendVoice(self.token, self.endpoint, chat_id, file, file_id, reply_message_id, forward_chat_id, forward_message_id, inline_keyboard_markup)

    async def removeMembers(self, chat_id: str, members: typing.Union[list[typing.Union[str, int]], str, int]) -> bool:
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
        return await removeMembers(self.token, self.endpoint, chat_id, members_dict)

    async def getChatInfo(self, chat_id: str) -> dict:
        return await getChatInfo(self.token, self.endpoint, chat_id)

    async def getChatAdmins(self, chat_id: str) -> list[dict]:
        return await getChatAdmins(self.token, self.endpoint, chat_id)
    
    async def getChatMembers(self, chat_id: str) -> list[dict]:
        return await getChatMembers(self.token, self.endpoint, chat_id)

    async def getChatBlockedUsers(self, chat_id: str) -> list[dict]:
        return await getChatBlockedUsers(self.token, self.endpoint, chat_id)

    async def getPendingMembers(self, chat_id: str) -> list[dict]:
        return await getPendingMembers(self.token, self.endpoint, chat_id)

    async def blockChatUser(self, chat_id: str, user_id: str, delete_last_messages: bool=False) -> bool:
        return await blockChatUser(self.token, self.endpoint, chat_id, user_id, delete_last_messages)
    
    async def unblockChatUser(self, chat_id: str, user_id: str) -> bool:
        return await unblockChatUser(self.token, self.endpoint, chat_id, user_id)

    async def resolvePendingUsers(self, chat_id: str, approve: bool, user_id: str="", everyone: bool=False) -> bool:
        return await resolvePendingUsers(self.token, self.endpoint, chat_id, approve, user_id, everyone)
    
    async def setGroupName(self, chat_id: str, new_name: str) -> bool:
        return await setGroupName(self.token, self.endpoint, chat_id, new_name)

    async def setGroupAbout(self, chat_id: str, about: str) -> bool:
        return await setGroupAbout(self.token, self.endpoint, chat_id, about)

    async def setGroupRules(self, chat_id: str, rules: str) -> bool:
        return await setGroupRules(self.token, self.endpoint, chat_id, rules)

    async def pinMessage(self, chat_id: str, message_id: str) -> bool:
        return await pinMessage(self.token, self.endpoint, chat_id, message_id)

    async def unpinMessage(self, chat_id: str, message_id: str) -> bool:
        return await unpinMessage(self.token, self.endpoint, chat_id, message_id)


if __name__ == "__main__":
    ...
