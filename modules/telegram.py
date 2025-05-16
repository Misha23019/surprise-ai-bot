from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from modules.router import handle_message, handle_settings
from modules.database import init_user
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # помести токен в .env или переменные окружения

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await init_user(user_id)
    await context.bot.send_message(chat_id=user_id, text="🌍 Оберіть мову / Choose language:", reply_markup=await handle_settings(user_id, "lang"))

async def message_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text
    await handle_message(user_id, text, context)

async def start_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    await app.initialize()
    await app.start()
    print("🤖 Бот запущен")
    await app.updater.start_polling()
