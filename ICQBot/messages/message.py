import typing

from ..ext.parseModes import *
from ..ext.Keyboards import InlineKeyboardMarkup
from .payloads import *
from ..ext.util import CustomDict


class SentMessage(CustomDict):
    def __init__(self, message_data: dict, bot_instance) -> None:
        self.bot_instance = bot_instance
        self.message_id = message_data['msgId']
        self.status = message_data['ok']
        self.chat_id = message_data['chat_id']
        self.text = message_data['text']
        if 'reply_message_id' in message_data:
            self.reply_message_id = message_data['reply_message_id']
        if 'forward_chat_id' in message_data:
            self.forward_chat_id = message_data['forward_chat_id']
        if 'forward_message_id' in message_data:
            self.forward_message_id = message_data['forward_message_id']

    async def edit(self, text: str, inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting(), parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()):
        edited_message: dict[str, typing.Any] = await self.bot_instance.editMessage(self.chat_id, self.message_id, text, inline_keyboard_markup, formatting, parse_mode)
        self.chat_id = edited_message['chat_id']
        self.text = edited_message['text']

    async def delete(self) -> None:
        deleted = await self.bot_instance.deleteMessage(self.chat_id, self.message_id)
        if deleted:
            self.token = None
            self.endpoint = None
            self.message_id = None
            self.status = None
            self.text = None
            if hasattr(self, "reply_message_id"):
                self.reply_message_id = None
            if hasattr(self, "forward_chat_id"):
                self.forward_chat_id = None
            if hasattr(self, "forward_message_id"):
                self.forward_message_id = None
        return None


class Author(CustomDict):
    def __init__(self, author_data: dict) -> None:
        if "firstName" in author_data:
            self.first_name = author_data['firstName']
        if "nick" in author_data:
            self.nickname = author_data['nick']
        if "lastName" in author_data:
            self.last_name = author_data['lastName']
        if "userId" in author_data:
            self.user_id = author_data["userId"]


class Payload(CustomDict):
    def __init__(self, payload_data, bot_instance=None) -> None:
        self.type = payload_data['type']
        self.payload: typing.Union[StickerPayload, FilePayload, None, MentionPayload, ReceivedMessage] = None
        # _payload_data: typing.Union[dict[typing.Any, typing.Any], str] = payload_data['payload']
        _payload_data = payload_data['payload']
        if self.type == "sticker":
            self.payload = StickerPayload(_payload_data["fileId"], "sticker")
        elif self.type == "file":
            self.payload = FilePayload(_payload_data['fileId'], _payload_data['type'])
        elif self.type == "mention":
            self.payload = MentionPayload(_payload_data["userId"], _payload_data['firstName'])
        elif self.type == "forward":
            self.payload = ReceivedMessage(_payload_data['message'], bot_instance)
        elif self.type == "reply":
            self.payload = ReceivedMessage(_payload_data['message'], bot_instance)


class ReceivedMessage(CustomDict):
    def __init__(self, message_data: dict, bot_instance) -> None:
        self.bot_instance = bot_instance
        self.chat_id: str = message_data['chat']['chatId']
        self.chat_type: str = message_data['chat']['type']
        self.chat_title: str = "Private conversation"
        if self.chat_type == "group":
            self.chat_title = message_data['chat']['title']
        self.author: Author = Author(message_data['from'])
        self.message_id: str = message_data['msgId']
        self.text: str = ""
        try:
            self.text = message_data['text']
        except KeyError:
            ...
        self.timestamp: int = message_data['timestamp']
        self.payloads = []
        try:
            for data in message_data['parts']:
                payload = Payload(data)
                self.payloads.append(payload)
        except Exception:
            pass

    async def reply(self, text: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting(), parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> SentMessage:
        return await self.bot_instance.sendText(self.chat_id, text, self.message_id, forward_chat_id, forward_message_id, inline_keyboard_markup, formatting, parse_mode)