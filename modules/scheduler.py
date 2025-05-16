from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging
import asyncio

from modules.database import get_all_users
from modules.telegram import send_message
from modules.lang import get_text

scheduler = BackgroundScheduler()

def send_surprise(user_id, lang):
    """Отправляет автосюрприз пользователю."""
    text = get_text("auto_surprise_text", lang) or "🎁 Ваш автосюрприз!"
    # send_message — асинхронная функция, вызываем через asyncio.run
    asyncio.run(send_message(user_id, text))

def send_daily_surprise():
    """Проверяет всех пользователей и отправляет автосюрприз в 10:00 по их локальному времени (упрощённо)."""
    users = get_all_users()
    now_utc = datetime.utcnow()

    for user in users:
        user_id = user['user_id']
        lang = user.get('language', 'en')
        user_time_str = user.get('surprise_time')  # ожидается формат "HH:MM"
        if not user_time_str:
            continue
        try:
            user_hour, user_minute = map(int, user_time_str.split(":"))
        except Exception:
            continue

        # Упрощённая логика: считаем, что user_time_str — время в UTC
        # Отправляем сюрприз, если сейчас ровно user_time_str (например 10:00)
        if now_utc.hour == user_hour and now_utc.minute == user_minute == 0:
            send_surprise(user_id, lang)

def start_scheduler():
    """Запускает планировщик, который вызывает send_daily_surprise каждую минуту."""
    scheduler.add_job(send_daily_surprise, 'interval', minutes=1)
    scheduler.start()
    logging.info("Scheduler started.")

def schedule_daily_surprises():
    """Обёртка для совместимости с app.py."""
    start_scheduler()
