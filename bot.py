import enel
import logging
import os

from telegram import Bot
from telegram.ext import CommandHandler, Dispatcher

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def enel(bot, update):
    reply = update.message.reply_text
    """ Command have form: /enel <cpf> <instalacao>"""
    arguments = update.message.split()
    if (len(arguments) is not 3):
        reply('Por favor, informe o CPF e numero de instalacao')
        return

    cpf, instalacao = arguments[1:] 
    try: 
        invoices = enel.get_invoices_pretty_print({'cpf':cpf, 'instalacao':instalacao})
        reply('Aqui estão suas faturas em aberto')
        for invoice in invoices:
            reply(invoice)
    except:
        reply('Não foi possível consultar as faturas. Tente novamente mais tarde.')


token = os.getenv('TELEGRAM_TOKEN')


def setup(token):
    # Create bot, update queue and dispatcher instances
    bot = Bot(token)

    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(CommandHandler('hello', hello))
    dispatcher.add_handler(CommandHandler('enel', enel))

    return bot, dispatcher
