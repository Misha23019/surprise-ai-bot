from apscheduler.schedulers.background import BackgroundScheduler
from modules.limits import reset_limits, increment_auto
from modules.telegram import send_message, build_keyboard
from modules.lang import get_user_lang, get_user_time
from modules.router import handle_message
from modules.database import get_all_users  # ти маєш реалізувати цю функцію
from datetime import datetime
import os
import logging

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def send_daily_surprise():
    users = get_all_users()
    now_utc = datetime.utcnow()

    for chat_id in users:
        user_time = get_user_time(chat_id)
        if not user_time:
            continue

        # Розрахунок годинної різниці між UTC і локальним часом користувача
        try:
            hours, minutes = map(int, user_time.split(":"))
        except:
            continue

        # Поточний час користувача = UTC + різниця (локальний час - 10:00)
        user_local_time = (now_utc.hour + hours - 10) % 24
        if user_local_time != 0:
            continue  # Не 10:00 за локальним часом

        lang = get_user_lang(chat_id) or "uk"
        surprise = handle_message(chat_id, "auto")
        increment_auto(chat_id)
        send_message(chat_id, surprise, TELEGRAM_TOKEN, build_keyboard(lang))

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_limits, "cron", hour=0, minute=0)  # кожного дня в 00:00 UTC
    scheduler.add_job(send_daily_surprise, "cron", minute=0)   # запускаємо щохвилини, перевіряємо 10:00
    scheduler.start()
    logging.info("✅ Планувальник запущено")
