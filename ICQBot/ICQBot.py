import asyncio
import aiohttp
import typing
from ICQBot.ext.actions import Action

from .mapper.MessagesMapper import (
    verifyToken,
    getBotInfo,
    sendText,
    editMessage,
    sendFile,
    getFileInfo,
    sendVoice,
)
from .ext.util import Response, sendGetRequest
from .mapper.ChatMapper import (
    sendAction,
    removeMembers,
    getChatInfo,
    getChatAdmins,
    getChatMembers,
    getChatBlockedUsers,
    getPendingMembers,
    blockChatUser,
    unblockChatUser,
    resolvePendingUsers,
    setGroupName,
    setGroupAbout,
    setGroupRules,
    pinMessage,
    unpinMessage,
)
from .messages.message import SentMessage
from .exceptions.ClientErrors import InvalidTokenError
from .ext.keyboards import InlineKeyboardMarkup


class ICQBot:
    def __init__(self, token: str) -> None:
        self.endpoint: str = "https://api.icq.net/bot/v1"
        self.token: str = token

    def setClientSession(self, session: aiohttp.ClientSession):
        self.session = session
        if (
            asyncio.get_event_loop().run_until_complete(
                verifyToken(self.session, self.token, self.endpoint)
            )
            is False
        ):
            self.logger.error("Invalid Token!")
            raise InvalidTokenError

    def info(self) -> dict[str, typing.Any]:
        """
        :return dict with information about the bot
        """
        return asyncio.get_event_loop().run_until_complete(
            getBotInfo(self.session, self.token, self.endpoint)
        )

    async def sendText(
        self,
        chat_id: str,
        text: str = "",
        reply_message_id: str = "",
        forward_chat_id: str = "",
        forward_message_id: str = "",
        inline_keyboard_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(),
        formatting: str = None,
        parse_mode: str = "MarkdownV2",
        action: typing.Union[None, Action] = None,
    ) -> SentMessage:
        """
        Sends a text message
        :param chat_id: the id of the chat
        :param text: the content of the message
        :param reply_message_id: the id of a message to be replyed
        :param forward_chat_id: the id of the chat where the message can be fw
        :param inline_keyboard_markup: keyboard markup to use with callbacks
        :param formatting: Formating of the message
        :param parse_mode: Parsing mode (MarkdownV2 or HTML)
        :param action: Action to be executed when the message sent
        :return: SentMessage object with the data of the sent message
        """
        if action is not None:
            await sendAction(self.session, self.token, self.endpoint, chat_id, action)
        return SentMessage(
            await sendText(
                self.session,
                self.token,
                self.endpoint,
                chat_id,
                text,
                reply_message_id,
                forward_chat_id,
                forward_message_id,
                inline_keyboard_markup,
                formatting,
                parse_mode,
            ),
            self,
        )

    async def editMessage(
        self,
        chat_id: str,
        message_id: str,
        text: str,
        inline_keyboard_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(),
        formatting: str = None,
        parse_mode: str = "MarkdownV2",
        action: typing.Union[None, Action] = None,
    ) -> dict[str, typing.Any]:
        """
        Edits a text message
        :param chat_id: the id of the chat
        :param text: the content of the message
        :param forward_chat_id: the if of the chat where the message can be fw
        :param inline_keyboard_markup: keyboard markup to use with callbacks
        :param formatting: Formating of the message
        :param parse_mode: Parsing mode (MarkdownV2 or HTML)
        :param action: Action to be executed when the message sent
        :return: object with the data of the sent message
        """
        if action is not None:
            sendAction(self.session, self.token, self.endpoint, chat_id, action)
        return await editMessage(
            self.session,
            self.token,
            self.endpoint,
            chat_id,
            message_id,
            text,
            inline_keyboard_markup,
            formatting,
            parse_mode,
        )

    async def sendFile(
        self,
        chat_id: str,
        file: typing.Union[str, bytes, None] = None,
        file_id: str = "",
        caption: str = "",
        reply_message_id: str = "",
        forward_chat_id: str = "",
        forward_message_id: str = "",
        inline_keyboard_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(),
        formatting: str = None,
        parse_mode: str = "MarkdownV2",
    ) -> dict[str, str]:
        return await sendFile(
            self.session,
            self.token,
            self.endpoint,
            chat_id,
            file,
            file_id,
            caption,
            reply_message_id,
            forward_chat_id,
            forward_message_id,
            inline_keyboard_markup,
            formatting,
            parse_mode,
        )

    async def getFileInfo(self, file_id: str) -> dict[str, typing.Any]:
        return await getFileInfo(self.session, self.token, self.endpoint, file_id)

    async def downloadFile(self, file_id: str) -> bytes:
        response: Response = await sendGetRequest(
            self.session, (await self.getFileInfo(file_id))["url"]
        )
        if response.status == 200:
            return response.content
        raise FileNotFoundError

    async def sendVoice(
        self,
        chat_id: str,
        file: typing.Union[str, bytes, None] = None,
        file_id: str = "",
        reply_message_id: str = "",
        forward_chat_id: str = "",
        forward_message_id: str = "",
        inline_keyboard_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(),
    ) -> dict[str, typing.Any]:
        return await sendVoice(
            self.session,
            self.token,
            self.endpoint,
            chat_id,
            file,
            file_id,
            reply_message_id,
            forward_chat_id,
            forward_message_id,
            inline_keyboard_markup,
        )

    async def removeMembers(
        self,
        chat_id: str,
        members: typing.Union[list[typing.Union[str, int]], str, int],
    ) -> bool:
        members_dict: list[dict[str, typing.Union[str, int]]] = []
        if isinstance(members, list):
            for member in members:
                members_dict.append({"sn": str(member)})
        elif isinstance(members, str):
            members_dict.append({"sn": members})
        else:
            raise TypeError("Invalid user!")
        return await removeMembers(
            self.session, self.token, self.endpoint, chat_id, members_dict
        )

    async def getChatInfo(self, chat_id: str) -> dict:
        return await getChatInfo(self.session, self.token, self.endpoint, chat_id)

    async def getChatAdmins(self, chat_id: str) -> list[dict]:
        return await getChatAdmins(self.session, self.token, self.endpoint, chat_id)

    async def getChatMembers(self, chat_id: str) -> list[dict]:
        return await getChatMembers(self.session, self.token, self.endpoint, chat_id)

    async def getChatBlockedUsers(self, chat_id: str) -> list[dict]:
        return await getChatBlockedUsers(
            self.session, self.token, self.endpoint, chat_id
        )

    async def getPendingMembers(self, chat_id: str) -> list[dict]:
        return await getPendingMembers(self.session, self.token, self.endpoint, chat_id)

    async def blockChatUser(
        self, chat_id: str, user_id: str, delete_last_messages: bool = False
    ) -> bool:
        return await blockChatUser(
            self.session,
            self.token,
            self.endpoint,
            chat_id,
            user_id,
            delete_last_messages,
        )

    async def unblockChatUser(self, chat_id: str, user_id: str) -> bool:
        return await unblockChatUser(
            self.session, self.token, self.endpoint, chat_id, user_id
        )

    async def resolvePendingUsers(
        self, chat_id: str, approve: bool, user_id: str = "", everyone: bool = False
    ) -> bool:
        return await resolvePendingUsers(
            self.session, self.token, self.endpoint, chat_id, approve, user_id, everyone
        )

    async def setGroupName(self, chat_id: str, new_name: str) -> bool:
        return await setGroupName(
            self.session, self.token, self.endpoint, chat_id, new_name
        )

    async def setGroupAbout(self, chat_id: str, about: str) -> bool:
        return await setGroupAbout(
            self.session, self.token, self.endpoint, chat_id, about
        )

    async def setGroupRules(self, chat_id: str, rules: str) -> bool:
        return await setGroupRules(
            self.session, self.token, self.endpoint, chat_id, rules
        )

    async def pinMessage(self, chat_id: str, message_id: str) -> bool:
        return await pinMessage(
            self.session, self.token, self.endpoint, chat_id, message_id
        )

    async def unpinMessage(self, chat_id: str, message_id: str) -> bool:
        return await unpinMessage(
            self.session, self.token, self.endpoint, chat_id, message_id
        )


if __name__ == "__main__":
    ...
