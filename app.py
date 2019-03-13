import bot
import json
import logging

from flask import Flask, request
from telegram import Update

app = Flask(__name__)
bot, dispatcher = bot.setup(bot.token)

logger = logging.getLogger(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/telegram", methods=['POST'])
def forward():
    payload = Update.de_json(request.json, bot)
    dispatcher.process_update(payload)
    return "ok"
    
