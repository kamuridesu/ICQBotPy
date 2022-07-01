try:
    from rawApiMessagesMapperFunctions import *
    from exceptions.ClientErrors import InvalidTokenError
    from Message import SentMessage
except ImportError:
    from .rawApiMessagesMapperFunctions import *
    from .Message import SentMessage
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

    def sendVoice(self, chat_id: str, file: typing.Union[str, bytes, None]=None, file_id: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup()) -> dict[str, typing.Any]:
        return sendVoice(self.token, self.endpoint, chat_id, file, file_id, reply_message_id, forward_chat_id, forward_message_id, inline_keyboard_markup)


if __name__ == "__main__":
    api_mapper = ICQBot("001.3476360037.4211413661:1004298326")
    message = api_mapper.sendText("@kamuridesu", "heloo gugulu")
    __import__("time").sleep(5)
    message.delete()
    # api_mapper.sendFile("@kamuridesu", file_id="0847P000fn3659v0PqH5NT62b5e5ef1ah", caption="repost")
