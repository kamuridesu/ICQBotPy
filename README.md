# ICQBOT

An actually working ICQ bot framework

- [Purpose](#purpose)
- [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Example](#example)
- [Current State](#current-state)
- [TODO](#todo)
- [NOTES](#notes)

## Purpose

I made this bot framework for personal use, since the original ICQ bot framework is a mess and
almost impossible to work with.

This bot allows for easy development and has a concise syntax based of Aiogram with a really simple
async impl.

## Getting started

### Installation

You can install this framework with the command `pip install ICQBot`.

### Example

[Checkout this example](example.py).

## Current state

The bot does not implements full control of the ICQ new api yet, I'll try to map the other
endpoints asap. The current implementations are:

- Self:
    - `/self/get`
- Chats:
    - `/chats/members/delete`
    - `POST /chats/avatar/set`
    - `/chats/sendActions`
    - `/chats/getInfo`
    - `/chats/getAdmins`
    - `/chats/getMembers`
    - `/chats/getBlockedUsers`
    - `/chats/getPendingUsers`
    - `/chats/blockUser`
    - `/chats/unblockUser`
    - `/chats/resolvePending`
    - `/chats/setTitle`
    - `/chats/setAbout`
    - `/chats/setRules`
    - `/chats/pinMessage`
    - `/chats/unpinMessage`
- Message:
    - `/messages/deleteMessages`
    - `/messages/sendText`
    - `/messages/editText`
    - `/messages/answerCallbackQuery`
    - `GET /messages/sendFile`
    - `POST /messages/sendFile`
    - `GET /messages/sendVoice`
    - `POST /messages/sendVoice`
- Files:
    - `/files/getInfo`
    - `/messages/sendFile`
- Events:
    - `/events/get`
        - `newMessage`
        - `callbackQuery`

## TODO

- Map all of the others endpoints
- Use matches with regex or string match to search for terms in messages

## Notes

There's a known bug on aiohttp on windows that closes the event loop. I'm trying to fix this rn.
