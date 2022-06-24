from typing import Any, Union


class Message:
	def __init__(self, message_data: dict[str, Any]) -> None:
		self.id = message_data['id']
