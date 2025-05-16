from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

from modules.database import get_all_users
from modules.telegram import send_message
from modules.lang import get_text

scheduler = BackgroundScheduler()

def send_daily_surprise():
    now_utc = datetime.utcnow()
    # Отправляем сюрприз всем в 10:00 UTC
    if now_utc.hour == 10 and now_utc.minute == 0:
        users = get_all_users()
        for user in users:
            user_id = user['user_id']
            lang = user.get('language', 'en')
            send_surprise(user_id, lang)
        logging.info(f"Sent daily surprise to {len(users)} users at {now_utc.isoformat()}")

def send_surprise(user_id, lang):
    text = get_text("auto_surprise_text", lang) or "🎁 Ваш автосюрприз!"
    send_message(user_id, text)

def start_scheduler():
    # Запускаем задачу, проверяющую каждую минуту
    scheduler.add_job(send_daily_surprise, 'interval', minutes=1)
    scheduler.start()
    logging.info("Scheduler started.")
