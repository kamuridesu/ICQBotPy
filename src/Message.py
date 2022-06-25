from typing import Any, Union


class Message(dict):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)