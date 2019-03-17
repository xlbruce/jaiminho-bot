import enel
import logging
import os

from random import random 

from telegram import Bot
from telegram.ext import CommandHandler, Dispatcher

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def hello(bot, update):
    reply = update.message.reply_text
    reply('Hello {} [{}]'.format(update.message.from_user.first_name, int(random() * 1000)))


def enel_handler(bot, update):
    reply = update.message.reply_text
    """ Command have form: /enel <cpf> <instalacao>"""
    arguments = update.message.text.split()
    if (len(arguments) is not 3):
        reply('Por favor, informe o CPF e numero de instalacao. Exemplo:')
        reply('/enel 12312312312 231472618')
        return

    cpf, instalacao = arguments[1:] 
    try: 
        invoices = enel.get_invoices_pretty_print({'cpf':cpf, 'instalacao':instalacao})
        if not invoices:
            reply('Não há faturas pendentes :smile:')
            return
        reply('Aqui estão suas faturas em aberto')
        for invoice in invoices:
            reply(invoice)
    except Exception as f:
        reply('Não foi possível consultar as faturas. Tente novamente mais tarde.')
        reply(f)


token = os.getenv('TELEGRAM_TOKEN')


def setup(token):
    # Create bot, update queue and dispatcher instances
    bot = Bot(token)

    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(CommandHandler('hello', hello))
    dispatcher.add_handler(CommandHandler('enel', enel_handler))

    return bot, dispatcher
