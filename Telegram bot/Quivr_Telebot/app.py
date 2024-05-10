import json
import logging
from config import tele_token, quivr_key, brain_id, prompt_id
import requests
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN=tele_token
quivr_url='https://api.quivr.app'   #NOTE for port, check your running Ollama port
model="gpt-3.5-turbo-0125"

def create_chatHandler(teleChatId):
    url=quivr_url+"/chat"
    headers={
        'Content-Type':'application/json',
        'Authorization':'Bearer '+quivr_key,
        'accept': 'application/json'
    }
    body={
        'name':teleChatId
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()['chat_id']

def get_chatid(teleChatId):
    url=quivr_url+"/chat"
    headers={
        'Content-Type':'application/json',
        'Authorization':'Bearer '+quivr_key
    }
    response = requests.get(url,headers=headers)
    for e in response.json()['chats']:
        if e['chat_name'] == teleChatId:
            return e['chat_id']
    return(create_chatHandler(teleChatId))

def chatbot(quest, teleChatId):
    headers={
        'Content-Type':'application/json',
        'Authorization':'Bearer '+quivr_key,
        'accept': 'application/json'
    }
    body={
        "question": quest,
  		"model": model,
  		"temperature": 0.7,
  		"max_tokens": 1000,
  		"brain_id": brain_id,
  		"prompt_id": prompt_id
    }
    chatid=get_chatid(str(teleChatId))
    url=f'{quivr_url}/chat/{chatid}/question?brain_id={brain_id}'
    response = requests.post(url, json=body, headers=headers)
    return json.dumps(response.json()['assistant'])
    

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi {update.effective_chat.username}, how can I help you?\nYou can also use '/help' command.")

async def quivr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respon = chatbot(update.message.text, update.effective_chat.id)
    respon=bytes(respon, 'utf-8').decode('unicode_escape')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=respon.strip("\""))

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respon="List of commands:\n\n1. /start : to see start page\n2. /help : to see this help\n\nAll other text will be responded by AI engine; Might give a bit slow response, please be patience."
    respon=bytes(respon, 'utf-8').decode('unicode_escape')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=respon)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), quivr))

    application.run_polling()
