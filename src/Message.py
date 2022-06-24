from typing import Any, Union


class Message:
	def __init__(self, message_data: dict[str, Any]) -> None:
		print(message_data)
		self.data = message_data