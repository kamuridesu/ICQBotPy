import typing

from ..mapper.MessagesMapper import deleteMessage, editMessage
from ..ext.parseModes import *
from ..ext.Keyboards import InlineKeyboardMarkup
from .payloads import *


class SentMessage:
    def __init__(self, message_data: dict, token: str, endpoint: str) -> None:
        self.token = token
        self.endpoint = endpoint
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

    def edit(self, text: str, inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()):
        edited_message: dict[str, typing.Any] = editMessage(self.token, self.endpoint, self.chat_id, self.message_id, text, inline_keyboard_markup, formatting, parse_mode)
        self.chat_id = edited_message['chat_id']
        self.text = edited_message['text']

    def delete(self) -> bool:
        deleted = deleteMessage(self.token, self.endpoint, self.chat_id, self.message_id)
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

    def __dict__(self) -> dict:
        d: dict = {
            "message_id": self.message_id,
            "status": self.status,
            "chat_id": self.chat_id,
            "text": self.text,
        }
        if hasattr(self, "reply_message_id"):
            d.update({"reply_message_id": self.reply_message_id})
        if hasattr(self, "forward_chat_id"):
            d.update({"forward_chat_id": self.forward_chat_id})
        if hasattr(self, "forward_message_id"):
            d.update({"forward_message_id": self.forward_message_id})
        return d

    @property
    def __str__(self) -> str:
        return self.__dict__.__str__()

    def __repr__(self) -> str:
        return self.__dict__.__repr__()



class Author:
    def __init__(self, first_name: str, user_id: str, nickname: str='', last_name: str='') -> None:
        self.first_name = first_name
        if nickname != '':
            self.nickname = nickname
        if last_name != '':
            self.last_name = last_name
        self.user_id = user_id

    @property
    def __dict__(self) -> dict:
        d = {
            "first_name": self.first_name,
            "user_id": self.user_id
        }
        if hasattr(self, "nickname"):
            d.update({"nickname": self.nickname})
        if hasattr(self, "last_name"):
            d.update({"last_name": self.last_name})
        return d

    def __str__(self) -> str:
        return self.__dict__.__str__()

    def __repr__(self) -> str:
        return self.__dict__.__repr__()


class Payload:
    def __init__(self, payload_data: dict[str, str], bot_instance=None) -> None:
        self.type = payload_data['type']
        self.payload: typing.Union[StickerPayload, FilePayload, None] = None
        payload_data = payload_data['payload']
        if self.type == "sticker":
            self.payload = StickerPayload(payload_data["fileId"])
        elif self.type == "file":
            self.payload = FilePayload(payload_data['fileId'])
        elif self.type == "mention":
            self.payload = MentionPayload(payload_data["userId"], payload_data['firstName'])
        elif self.type == "forward":
            self.payload = ReceivedMessage(payload_data['message'], bot_instance)
        elif self.type == "reply":
            self.payload = ReceivedMessage(payload_data['message'], bot_instance)

    @property
    def __dict__(self) -> dict:
        return {
            "type": self.type,
            "payload": self.payload.__dict__
        }

    def __str__(self) -> str:
        return self.__dict__.__str__()
    
    def __repr__(self) -> str:
        self.__str__()


class ReceivedMessage:
    def __init__(self, message_data: dict, bot_instance) -> None:
        self.bot_instance = bot_instance
        self.chat_id: str = message_data['payload']['chat']['chatId']
        self.chat_type: str = message_data['payload']['chat']['type']
        self.chat_title: str = "Private conversation"
        if self.chat_type == "group":
            self.chat_title = message_data['payload']['chat']['title']
        author_info: str = message_data['payload']['from']
        nick = ""
        if "nick" in author_info:
            nick = author_info['nick']
        self.author: str = Author(author_info['firstName'], author_info['userId'], nick)
        self.message_id: str = message_data['payload']['msgId']
        try:
            self.text: str = message_data['payload']['text']
        except KeyError:
            self.text: str = ""
        self.timestamp: int = message_data['payload']['timestamp']
        try:
            self.payloads = []
            for data in message_data['payload']['parts']:
                payload = Payload(data)
                self.payloads.append(payload)
        except Exception:
            pass

    def reply(self, text: str, forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> SentMessage:
        return self.bot_instance.sendText(self.chat_id, text, self.message_id, forward_chat_id, forward_message_id, inline_keyboard_markup, formatting, parse_mode)

    @property
    def __dict__(self) -> dict:
        d: dict = {
            "message_id": self.message_id,
            "chat_id": self.chat_id,
            "text": self.text,
            "chat_type": self.chat_type,
            "chat_title": self.chat_title,
            "author": self.author.__dict__,
            "message_id": self.message_id,
            "text": self.text,
            "timestamp": self.timestamp
        }
        if hasattr(self, "payloads"):
            d.update({"payloads": [x.__dict__ for x in self.payloads]})
        return d

    def __str__(self) -> str:
        return self.__dict__.__str__()

    def __repr__(self) -> str:
        return self.__dict__.__repr__()
