import typing

from rawApiMessagesMapperFunctions import deleteMessage

try:
	from rawApiMessagesMapperFunctions import editMessage
	from parseModes import *
	from Keyboards import InlineKeyboardMarkup
except ImportError:
	from .rawApiMessagesMapperFunctions import editMessage
	from .parseModes import *
	from .Keyboards import InlineKeyboardMarkup


class Message:
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

	def __str__(self) -> str:
		return self.__dict__().__str__()

	def __repr__(self) -> str:
		return self.__dict__().__repr__()
