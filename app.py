import logging
import os
import sys
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
from modules.scheduler import start_scheduler  # Предполагаем, что это async

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_bot(update.effective_user.id, context)

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from modules.router import handle_message
    await handle_message(update.effective_user.id, update.message.text, context)


def main():
    if sys.platform == "win32":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    import asyncio

    # Запускаем async функцию планировщика, не блокируя основной поток
    loop = asyncio.get_event_loop()
    loop.create_task(start_scheduler())

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message))

    print("🤖 Бот запущен.")
    app.run_polling()  # запускаем синхронно


if __name__ == "__main__":
    main()
