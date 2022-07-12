from .message import ReceivedMessage
from .message import Author
from ..ext.util import CustomDict


class Callback(CustomDict):
    def __init__(self, data: dict, bot_instance) -> None:
        self.author = Author(data['from'])
        self.message_data: ReceivedMessage = ReceivedMessage(data['message'], bot_instance)
        self.query_id: str = data['queryId']
        for attr in data:
            if not hasattr(self, attr):
                if attr not in ["message", "from", "queryId"]:
                    self.__setattr__(attr, data[attr])
