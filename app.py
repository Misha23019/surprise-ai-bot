import os
from flask import Flask, request, abort
from telegram import Update, Bot
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler, 
    ContextTypes, 
    filters
)
from modules.router import start, time_handler, button_handler, language_selection_handler
from modules.scheduler import start_scheduler

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in environment variables")

app = Flask(__name__)

# Создаем объект Application (асинхронный аналог Dispatcher)
application = Application.builder().token(TOKEN).build()

# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(language_selection_handler, pattern=r"^lang_"))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, time_handler))

@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
        return "OK"
    else:
        abort(400)

if __name__ == "__main__":
    # Запускаем планировщик
    start_scheduler()

    # Устанавливаем вебхук вручную (можно через Telegram API)
    # await application.bot.set_webhook("https://yourserver.com/webhook")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
