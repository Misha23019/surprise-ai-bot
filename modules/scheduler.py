from datetime import datetime
import pytz
import logging

from modules.database import get_all_users
from modules.telegram import send_message
from modules.lang import get_text

def send_daily_surprise(context):
    now_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
    users = get_all_users()

    for user in users:
        user_id = user['user_id']
        lang = user.get('language', 'en')
        user_time_str = user.get('surprise_time')
        user_timezone_str = user.get('timezone', 'UTC')

        if not user_time_str:
            continue

        try:
            user_hour, user_minute = map(int, user_time_str.split(":"))
        except Exception as e:
            logging.warning(f"Invalid surprise_time format for user {user_id}: {e}")
            continue

        try:
            user_tz = pytz.timezone(user_timezone_str)
        except Exception:
            user_tz = pytz.UTC

        # Конвертуємо поточний час UTC в локальний
        user_local_time = now_utc.astimezone(user_tz)

        if user_local_time.hour == user_hour and user_local_time.minute == user_minute:
            send_surprise(user_id, lang)
            logging.info(f"Sent surprise to user {user_id} at {user_local_time.isoformat()} ({user_timezone_str})")

def send_surprise(user_id, lang):
    text = get_text("auto_surprise_text", lang) or "🎁 Ваш автосюрприз!"
    send_message(user_id, text)

def start_scheduler(job_queue):
    # Виконувати щохвилини (ти вже перевіряєш час вручну)
    job_queue.run_repeating(send_daily_surprise, interval=60, first=0)
