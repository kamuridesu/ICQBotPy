
from aiohttp import ServerDisconnectedError
import requests
import typing
import json

try:
    from exceptions.ClientErrors import ClientError
    from exceptions.GenericErrors import NotExpectedError
    from parseModes import *
    from Keyboards import *
except ImportError:
    from .exceptions.ClientErrors import ClientError
    from .exceptions.GenericErrors import NotExpectedError
    from .parseModes import *
    from .Keyboards import *


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

    def sendText(self, chat_id: str, text: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), format: Formatting=Formatting, parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default) -> dict[str, str]:
        route = "/messages/sendText?"
        query = f"token={self.token}&chatId={chat_id}&text={text}&replyMsgId={reply_message_id}&forwardChatId={forward_chat_id}&forwardMsgId={forward_message_id}&inlineKeyboardMarkup={inline_keyboard_markup.getButtonsAsString()}&format={format.content}&parseMode={parse_mode}"
        print(query)


if __name__ == "__main__":
    api_mapper = RawApiMapper("001.1917418351.1245850609:1004146438")
    # print(api_mapper.verifyToken())
    api_mapper.sendText("normienette")