from ICQBot import ICQBot, Dispatcher
from ICQBot.ext import ReceivedMessage


bot = ICQBot("TOKEN")
dp = Dispatcher(bot)


@dp.message_handler(commands="/echo")
def test(message: ReceivedMessage):
    print(message)
    return message.reply(''.join(message.text.split(' ')[1:]))


if __name__ == "__main__":
    dp.start_polling()