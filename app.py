import os
import logging
from flask import Flask, request
from telegram import Update
from modules.telegram import bot, dispatcher
from modules.scheduler import schedule_daily_surprises

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def index():
    return "Surprise Me! bot is running."

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    except Exception as e:
        logging.error(f"Error handling update: {e}")
    return "OK"

if __name__ == "__main__":
    # Установка вебхука (если нужно — опционально)
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Пример: https://your-app.onrender.com/telegram
    if WEBHOOK_URL:
        bot.set_webhook(url=WEBHOOK_URL)
        logging.info(f"Webhook set to: {WEBHOOK_URL}")
    else:
        logging.warning("WEBHOOK_URL not set. Webhook not configured.")

    # Запускаем планировщик
    schedule_daily_surprises()

    # Запускаем Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
