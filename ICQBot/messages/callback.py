from .message import ReceivedMessage
from .message import Author
from ..ext.util import CustomDict
from ..mapper.MessagesMapper import answerCallbackQuery


class Callback(CustomDict):
    def __init__(self, data: dict, bot_instance) -> None:
        self.bot_instance = bot_instance
        self.author = Author(data['from'])
        self.message_data: ReceivedMessage = ReceivedMessage(data['message'], bot_instance)
        self.query_id: str = data['queryId']
        for attr in data:
            if not hasattr(self, attr):
                if attr not in ["message", "from", "queryId"]:
                    self.__setattr__(attr, data[attr])

    def answer(self, text: str="", show_alert: bool=False) -> bool:
        url = ""
        if hasattr(self, 'url'):
            url = self.url
        return answerCallbackQuery(self.bot_instance.token, self.bot_instance.endpoint, self.query_id, text, show_alert, url)
