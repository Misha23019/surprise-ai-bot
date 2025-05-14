from apscheduler.schedulers.background import BackgroundScheduler
import random
from telegram import send_message
from lang import user_langs

content_list = [
    "🎬 Рандомний фільм", "🎧 Музика", "📚 Цитата або уривок з книги",
    "🌐 Маловідомий сайт", "🧠 Цікавий факт", "😂 Жарт / цитата",
    "🕵️ Містичний контент", "🖼️ Мистецтво", "🎙️ Подкаст / YouTube",
    "🎯 Щоденне завдання", "🧵 Історія", "💭 Тема дня", "🍲 Рецепт"
]

def send_random_post():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    for chat_id in user_langs:
        msg = random.choice(content_list)
        send_message(chat_id, msg, TELEGRAM_TOKEN)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_random_post, 'interval', days=1, start_date='2025-05-15 10:00:00')
    scheduler.start()
