import asyncio
import logging
from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

from modules.telegram import start_bot
from modules.scheduler import start_scheduler

# Настройка логгера
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_bot(update.effective_user.id, context)

# Обработчик всех входящих сообщений
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from modules.router import handle_message
    await handle_message(update.effective_user.id, update.message.text, context)

# Основной запуск
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message))

    # Запуск планировщика авторассылки
    await start_scheduler()

    # Запуск бота
    print("🤖 Бот запущен.")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
