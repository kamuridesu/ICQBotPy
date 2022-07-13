import aiohttp
import typing
import os

from ..exceptions.GenericErrors import NotExpectedError
from ..exceptions.MessageErrors import MessageNotSentError, FileTypeMismatchError, AmbigousFileError, MessageNotDeletedError, CallbackAnswerError

from ..ext.parseModes import Formatting, HtmlMarkup, Markdown
from ..ext.Keyboards import InlineKeyboardMarkup
from ..ext.util import fetcher, Response


async def getBotInfo(token: str, endpoint: str) -> dict[str, typing.Any]:
    response: Response = await fetcher("get", endpoint + "/self/get?token=" + token)

    if response and response.status == 200:
        return (await response.json())
    raise NotExpectedError("Server response is empty or invalid!")


async def verifyToken(token: str, endpoint: str) -> bool:
    info: dict[str, typing.Any] = await getBotInfo(token, endpoint)
    return info['ok']


async def sendText(token: str, endpoint: str, chat_id: str, text: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting(), parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> dict[str, str]:
    route = "/messages/sendText?"
    query = f"token={token}&chatId={chat_id}&parseMode={parse_mode.content}"
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
    response: Response = await fetcher("get", endpoint + route + query)
    if response.status == 200:
        response_dict: dict = (await response.json())
        if response_dict['ok']:
            response_dict.update({
                "chat_id": chat_id,
                "text": text,
                "reply_message_id": reply_message_id,
                "forward_chat_id": forward_chat_id,
                "forward_message_id": forward_message_id,
            })
            return response_dict
        raise MessageNotSentError(response_dict['description'])
    raise MessageNotSentError


async def editMessage(token: str, endpoint: str, chat_id: str, message_id: str, text: str, inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting(), parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> dict[str, typing.Any]:
    route = "/messages/editText?"
    query = f"&token={token}&chatId={chat_id}&msgId={message_id}&text={text}&parseMode={parse_mode.content}"
    if inline_keyboard_markup.getButtonsAsString():
        query += f"&inlineKeyboardMarkup={inline_keyboard_markup.getButtonsAsString()}"
    if formatting.content:
        query += f"&format={formatting.content}"

    response: Response = await fetcher("get", endpoint + route + query)

    if response.status == 200:
        response_dict: dict = (await response.json())
        if response_dict['ok']:
            response_dict.update({
                "chat_id": chat_id,
                "text": text,
            })
            return response_dict
        raise MessageNotSentError(response_dict['description'])
    raise MessageNotSentError


async def uploadFile(endpoint: str, route: str, query: str, file_id: typing.Union[str, None]=None, file: typing.Union[str, bytes, None]=None) -> Response:
    response: typing.Union[None, Response] = None
    if file_id:
        query += f"&fileId={file_id}"
        response = await fetcher("get", endpoint + route + query)
    elif file:
        content: typing.Union[dict[str, tuple[str, bytes]], None] = None
        if isinstance(file, bytes):
            content = {'file': ('noname', file)}
        elif isinstance(file, str):
            if not os.path.isfile(file):
                raise FileNotFoundError
            with open(file, "rb") as file_bytes:
                content = {'file': (os.path.basename(file), file_bytes.read())}
        if content is None:
            raise FileTypeMismatchError
        response = await fetcher("post", endpoint + route + query, files=content)
    if response is not None:
        return response
    raise NotExpectedError("File cannot be uploaded! Cause unknown")


async def sendFile(token: str, endpoint: str, chat_id: str, file: typing.Union[str, bytes, None]=None, file_id: str="", caption: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup(), formatting: Formatting=Formatting(), parse_mode: typing.Union[Markdown, HtmlMarkup]=Markdown.default()) -> dict[str, str]:
    route = "/messages/sendFile?"
    query = f"token={token}&chatId={chat_id}&parseMode={parse_mode.content}"
    response: typing.Union[Response, None] = None
    if file_id and file:
        raise AmbigousFileError
    if file_id == "" and file == None:
        raise FileNotFoundError
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
    
    response = uploadFile(endpoint, route, query, file_id, file)
        
    if response.status == 200:
        response_dict: dict = (await response.json())
        if response_dict['ok']:
            return response_dict
        raise MessageNotSentError(response_dict['description'])
    raise MessageNotSentError


async def sendVoice(token: str, endpoint: str, chat_id: str, file: typing.Union[str, bytes, None]=None, file_id: str="", reply_message_id: str="", forward_chat_id: str="", forward_message_id: str="", inline_keyboard_markup: InlineKeyboardMarkup=InlineKeyboardMarkup()) -> dict[str, typing.Any]:
    route = "/messages/sendVoice?"
    query = f"token={token}&chatId={chat_id}"
    response: typing.Union[Response, None] = None
    if file_id and file:
        raise AmbigousFileError
    if reply_message_id:
        query += f"&replyMsgId={reply_message_id}"
    if forward_chat_id:
        query += f"&forwardChatId={forward_chat_id}"
    if forward_message_id:
        query += f"&forwardMsgId={forward_message_id}"
    if inline_keyboard_markup.getButtonsAsString():
        query += f"&inlineKeyboardMarkup={inline_keyboard_markup.getButtonsAsString()}"
    
    response = uploadFile(endpoint, route, query, file_id, file)
        
    if response.status == 200:
        response_dict: dict = (await response.json())
        if response_dict['ok']:
            return response_dict
        raise MessageNotSentError(response_dict['description'])
    raise MessageNotSentError


async def getFileInfo(token: str, endpoint: str, file_id: str) -> dict[str, typing.Any]:
    route = "/files/getInfo?"
    query = f"token={token}&fileId={file_id}"

    response: Response = await fetcher("get", endpoint + route + query)

    if response.status == 200:
        return (await response.json())
    raise FileNotFoundError


async def deleteMessage(token: str, endpoint: str, chat_id: str, message_id: str) -> bool:
    route = "/messages/deleteMessages?"
    query = f"token={token}&chatId={chat_id}&msgId={message_id}"
    response: Response = await fetcher("get", endpoint + route + query)
    if response.status == 200:
        return (await response.json())['ok']    
    raise MessageNotDeletedError


async def answerCallbackQuery(token: str, endpoint: str, query_id: str, text: str="", show_alert: bool=False, url=""):
    route = "/messages/answerCallbackQuery?"
    query = f"token={token}&queryId={query_id}"
    if text:
        query += f"&text={text}"
    if show_alert:
        query += f"&showAlert={show_alert}"
    if url:
        query += f"&url={url}"

    response: Response = await fetcher("get", endpoint + route + query)
    if response.status == 200:
        return (await response.json())['ok']
    raise CallbackAnswerError
