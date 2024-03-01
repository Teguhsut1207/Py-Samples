TOKEN = 'YOUR-API-TOKEN'
#------------------------
import json
import logging

import requests
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

Ollama_url='http://localhost:11434/api/generate'   #NOTE for port, check your running Ollama port

def chatbot(quest):
    headers={
        'Content-Type':'cpplication/json'
    }

    body={
        'model':'llama2',
        'prompt':str(quest),
        'stream':False
    }
    response = requests.post(Ollama_url, json=body, headers=headers)
    return json.dumps(response.json()['response'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {update.effective_chat.username}, how can I help you?\nYou can also use '/help' command.")

async def ollama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respon = chatbot(update.message.text)
    respon=bytes(respon, 'utf-8').decode('unicode_escape')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=respon.strip("\""))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respon="List of commands:\n\n1. /start : to see start page\n2. /help : to see this help\n\nAll other text will be responded by Llama2 which is an LLM engine; Might give a bit slow response, please be patience."
    respon=bytes(respon, 'utf-8').decode('unicode_escape')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=respon)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ollama))

    application.run_polling()