from ICQBot import ICQBot, Dispatcher
from ICQBot.ext import ReceivedMessage


bot = ICQBot("TOKEN")
dp = Dispatcher(bot)


# to repeat a message
@dp.message_handler(commands="/echo")
def test(message: ReceivedMessage):
    print(message)
    return message.reply(' '.join(message.text.split(' ')[1:]))


# to ban an user
@dp.message_handler(commands=["/ban"])
def ban(message: ReceivedMessage):
    user_to_ban = message.payloads[-1].payload.user_id
    return print(bot.removeMembers(message.chat_id, user_to_ban))


if __name__ == "__main__":
    dp.start_polling()
