from ICQBot import ICQBot, Dispatcher, executor
from ICQBot.messages import ReceivedMessage
from ICQBot.messages.callback import Callback
from ICQBot.ext.keyboards import InlineKeyboardMarkup, Button


bot = ICQBot("TOKEN")
dp = Dispatcher(bot)


# to repeat a message
@dp.message_handler(commands="")
async def test(message: ReceivedMessage):
    return message.reply(message.text)


# to ban an user
@dp.message_handler(commands=["/ban"])
async def ban(message: ReceivedMessage):
    payload = message.payloads[-1].payload
    user_to_ban = payload.user_id  # type: ignore
    return print(bot.removeMembers(message.chat_id, user_to_ban))


# Keyboard
@dp.message_handler(commands="/start")
async def start(message: ReceivedMessage):
    keyboard = InlineKeyboardMarkup()
    keyboard.addButton(Button(text="Hello", callbackData="World"))
    keyboard.addRow()
    keyboard.addButton(Button(text="Bye", callbackData="Ok"), row=1)
    return await message.reply("Ola", inline_keyboard_markup=keyboard)


# callback handlers
@dp.callback_query_handler(context="callbackData", value="World")
async def answer_world(callback: Callback):
    await bot.sendText(callback.message_data.chat_id, "Nyahello")
    return await callback.answer(f"Hello {callback.callbackData}")


@dp.callback_query_handler(context="callbackData", value="Ok")
async def answer_ok(callback: Callback):
    await bot.sendText(callback.message_data.chat_id, "Orayo")
    return await callback.answer("No")


if __name__ == "__main__":
    executor(dp)
