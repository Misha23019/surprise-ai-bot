# modules/telegram.py

import os
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.ext import ApplicationBuilder

from modules.router import start_command, handle_callback_query, handle_text

# Инициализация Telegram Bot
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in environment variables")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
dispatcher = application.dispatcher

# Регистрация команд и кнопок
dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(CallbackQueryHandler(handle_callback_query))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Прямо из этого модуля экспортируем application, чтобы запускать polling/webhook
__all__ = ["bot", "application"]
