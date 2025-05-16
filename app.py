import logging
import os
import sys
import asyncio
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

from modules.telegram import start_bot
from modules.router import handle_message
from modules.scheduler import start_scheduler  # 👈 добавляем правильный импорт

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_bot(update.effective_user.id, context)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_message(update.effective_user.id, update.message.text, context)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Регистрируем хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message))

    print("🤖 Бот запущен.")

    # ✅ Запускаем планировщик (sync-функция, передаём app)
    start_scheduler(app)

    await app.run_polling()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
