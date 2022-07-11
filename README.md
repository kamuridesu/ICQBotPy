# ICQBOT
An actually working ICQ bot framework

## Purpose
I made this bot framework for personal use, since the original ICQ bot framework is a mess and almost impossible to work with.

This bot allows for easy development and has a concise syntax based of Aiogram (although no async implementation yet).

## Example
(example.py)[!Example]


## Current state
The bot does not implements full control of the ICQ new api yet, I'll try to map the other endpoints asap. The current implementations are:
- Chats:
	- /chats/members/delete
- Message:
	- /messages/deleteMessages
	- /messages/sendText
	- /messages/editText
- Files:
	- /files/getInfo
	- /messages/sendFile
- Events:
	- /events/get
		- newMessage


## TODO
- Map all of the others endpoints
- Use matches with regex or string match to search for terms in messages[1]
- Impl async


[1] ```python
@dp.message_handler("regex_pattern")
```

