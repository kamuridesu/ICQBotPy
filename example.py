from ICQBot import ICQBot, Dispatcher, executor
from ICQBot.messages import ReceivedMessage
from ICQBot.messages.callback import Callback
from ICQBot.ext.Keyboards import InlineKeyboardMarkup, Button
from ICQBot.messages.payloads import FilePayload, StickerPayload


bot = ICQBot("TOKEN")
dp = Dispatcher(bot)


# to repeat a message
@dp.message_handler()
async def test(message: ReceivedMessage):
    print(message)
    return message.reply(message.text)


# to ban an user
@dp.message_handler(commands=["/ban"])
async def ban(message: ReceivedMessage):
    classes_without_id: list = [StickerPayload, FilePayload, None, ReceivedMessage]
    payload = message.payloads[-1].payload
    if all([not isinstance(payload, x) for x in classes_without_id]):
        user_to_ban = payload.user_id # type: ignore
        return print(bot.removeMembers(message.chat_id, user_to_ban))


# Keyboard
@dp.message_handler(commands="/start")
async def start(message: ReceivedMessage):
    keyboard = InlineKeyboardMarkup()
    keyboard.addButton(Button(text="Hello", callbackData="World"))
    keyboard.addRow()
    keyboard.addButton(Button(text="Bye", callbackData="Ok"), row=1)
    return message.reply("Ola", inline_keyboard_markup=keyboard)


# callback handlers
@dp.callback_query_handler(context="callbackData", value="World")
async def answer_world(callback: Callback):
    return callback.answer(f"Hello " + callback.callbackData)


@dp.callback_query_handler(context="callbackData", value="Ok")
async def answer_ok(callback: Callback):
    return callback.answer("No")


if __name__ == "__main__":
    executor(dp)
