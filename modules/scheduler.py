from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging
import asyncio
import pytz

from modules.database import get_all_users
from modules.telegram import send_message
from modules.lang import get_text

scheduler = BackgroundScheduler()

def send_surprise(user_id, lang):
    """Отправляет автосюрприз пользователю."""
    text = get_text("auto_surprise_text", lang) or "🎁 Ваш автосюрприз!"
    asyncio.run(send_message(user_id, text))

def send_daily_surprise():
    """Проверяет всех пользователей и отправляет автосюрприз в 10:00 по их локальному времени."""
    users = get_all_users()
    now_utc = datetime.utcnow()

    for user in users:
        user_id = user['user_id']
        lang = user.get('language', 'en')
        user_time_str = user.get('surprise_time')  # формат "HH:MM"
        if not user_time_str:
            continue
        try:
            user_hour, user_minute = map(int, user_time_str.split(":"))
        except Exception:
            continue

        if now_utc.hour == user_hour and now_utc.minute == user_minute == 0:
            send_surprise(user_id, lang)

def start_scheduler():
    """Запускает планировщик, если он ещё не запущен."""
    if not scheduler.running:
        scheduler.add_job(send_daily_surprise, 'interval', minutes=1, timezone=pytz.UTC)
        scheduler.start()
        logging.info("Scheduler started.")
    else:
        logging.info("Scheduler already running. Skipping start.")

def schedule_daily_surprises():
    """Обёртка для app.py."""
    start_scheduler()
