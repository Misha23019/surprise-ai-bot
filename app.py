from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher
import os
import logging

from modules.router import start_command, handle_text, handle_callback_query
from modules.scheduler import schedule_daily_surprises
from modules.database import init_db, reset_manual_counts_if_needed
from modules.telegram import bot  # Импорт уже настроенного бота

app = Flask(__name__)

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация базы данных
init_db()
reset_manual_counts_if_needed()

# Планировщик
schedule_daily_surprises()

# Инициализация диспетчера
dispatcher = Dispatcher(bot, None, workers=4, use_context=True)
dispatcher.add_handler(start_command)
dispatcher.add_handler(handle_text)
dispatcher.add_handler(handle_callback_query)

# 🚨 ВОТ ЭТО ГЛАВНОЕ: маршрут Telegram вебхука
@app.route('/telegram', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# Если хочешь простой ответ на GET /
@app.route('/')
def index():
    return 'Surprise Me Bot is running.'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
