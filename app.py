import logging
import os
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
from modules.scheduler import start_scheduler  # <--- не забудь!
from modules.router import handle_message

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_bot(update.effective_user.id, context)

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_message(update.effective_user.id, update.message.text, context)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message))

    # 👇 Планировщик — теперь как callback после старта
    async def post_init(application):
        await start_scheduler(application)

    app.post_init = post_init

    print("🤖 Бот запущен.")
    app.run_polling()  # ❌ НЕ await и НЕ asyncio.run

if __name__ == "__main__":
    main()
