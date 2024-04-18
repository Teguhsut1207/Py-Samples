import asyncio
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)

from aiohttp import web
from config import secret_token, tele_token, url
from telegram import Bot, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

# Replace with your actual Telegram bot token
BOT_TOKEN = tele_token
# Replace with your server URL where the webhook will be hosted
URL = url

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user.username
    if (user==None):user=update.effective_user.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi, {user}! How can I help you?")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def start_webhook(bot_token, webhook_url, host, port):
    """Sets the webhook for the bot and starts aiohttp server."""
    bot = Bot(token=bot_token)
    application = ApplicationBuilder().token(bot_token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    async def on_startup(app):
        await bot.initialize()
        await application.initialize()
        await bot.set_webhook(f"{webhook_url}/webhook")

    async def on_shutdown(app):
        await bot.delete_webhook()

    async def handle_update(request):
        if request.method == "POST":
            data = await request.json()
            try:
               update = Update.de_json(data, bot)
            except:
               logging.error(f'Unknown data received: {data} with header: {request.headers}')
            else:
               await application.process_update(update)
               return web.Response(text="OK")
        else:
            return web.Response(status=400)

    app = web.Application()
    app.router.add_post("/webhook", handle_update)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logging.info(f"Webhook server started at {webhook_url}")
    await asyncio.Future()  # Loop forever for continuous operation

if __name__ == "__main__":
    HOST = "localhost"  # Define your host
    PORT = 5001  # Define your port
    asyncio.run(start_webhook(BOT_TOKEN, URL, HOST, PORT))  # Pass the necessary arguments
