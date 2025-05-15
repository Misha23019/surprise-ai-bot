from apscheduler.schedulers.background import BackgroundScheduler
from modules.limits import reset_limits, increment_auto
from modules.telegram import send_message, build_keyboard
from modules.database import get_all_users
from modules.lang import get_user_lang, get_user_time, LANGUAGES
from modules.router import handle_message
from datetime import datetime
import logging
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def send_auto_surprise(chat_id):
    lang = get_user_lang(chat_id) or 'uk'  # дефолтна мова
    user_time = get_user_time(chat_id)
    if not user_time:
        return  # Якщо час не встановлено — не відправляємо

    # Перевірка, чи зараз 10:00 по годині користувача
    now_utc = datetime.utcnow()
    user_hour, user_minute = map(int, user_time.split(":"))
    # Обчислюємо, чи співпадає зараз час відправлення (10:00 користувача)
    # Для спрощення перевіримо тільки годину - можна уточнити по таймеру
    if now_utc.hour != user_hour:
        return

    # Перевіряємо, чи не перевищено ліміт (5 звичайних + 1 автопост = 6)
    if not increment_auto(chat_id):
        logging.info(f"Автопост для {chat_id} не відправлено: перевищено ліміт.")
        return

    reply = handle_message(chat_id, "/auto_surprise")  # або інша логіка автосюрпризу
    send_message(chat_id, reply, TELEGRAM_TOKEN, build_keyboard(lang))
    logging.info(f"Автопост для {chat_id} надіслано.")

def start_scheduler():
    scheduler = BackgroundScheduler()

    # Очищення лімітів о 00:00 UTC
    scheduler.add_job(reset_limits, "cron", hour=0, minute=0)

    # Автопости що хвилину (можна змінити частоту)
    scheduler.add_job(
        lambda: [send_auto_surprise(user) for user in get_all_users()],
        "interval", minutes=1
    )

    scheduler.start()
    logging.info("✅ Планувальник запущено")
