from .message import ReceivedMessage
from .message import Author
import typing


class Callback:
    def __init__(self, data: dict) -> None:
        self.payload = data['payload']
        if "from" in self.payload:
            self.author = Author(self.payload['from'])
        self.message_data = ReceivedMessage(data['message'])
        self.query_id = data['queryId']

        