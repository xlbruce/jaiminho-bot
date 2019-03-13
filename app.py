import bot
import json
import logging

from flask import Flask, request
from telegram import Update

app = Flask(__name__)
bot, dispatcher = bot.setup(bot.token)

@app.route("/")
def hello():
    return "Run <pre>curl https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}</pre> to setup Telegram Webhook."

@app.route("/telegram", methods=['POST'])
def forward():
    payload = Update.de_json(request.json, bot)
    dispatcher.process_update(payload)
    return "ok"
    
