import logging
import os

from telegram import Bot
from telegram.ext import CommandHandler, Dispatcher

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def hello(update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


token = os.getenv('TELEGRAM_TOKEN')


def setup(token):
    # Create bot, update queue and dispatcher instances
    bot = Bot(token)

    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(CommandHandler('hello', hello))

    ##### Register handlers here #####

    return bot, dispatcher
