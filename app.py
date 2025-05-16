import os
from flask import Flask, request, abort
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from modules.router import start, time_handler, button_handler
from modules.scheduler import start_scheduler, schedule_daily_surprises
from modules.database import reset_manual_counts

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in environment variables")

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# Регистрируем обработчики с правильными именами функций
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button_handler))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, time_handler))

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return "OK"
    else:
        abort(400)

if __name__ == "__main__":
    # Запускаем планировщик
    start_scheduler()
    # Переназначаем задачи из базы
    schedule_daily_surprises()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
