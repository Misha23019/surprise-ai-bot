from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from modules.database import get_all_users
from modules.telegram import send_message, build_keyboard
from modules.lang import get_user_lang, get_user_time, get_text
from modules.gpt_api import ask_gpt
from modules.limits import reset_limits, was_auto_sent, mark_auto_sent, increment_auto

import pytz
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

def send_daily_surprises():
    users = get_all_users()
    for user in users:
        user_id = user["id"]
        lang = get_user_lang(user_id)
        time_str = get_user_time(user_id)  # HH:MM
        texts = get_text(lang)
        
        if not time_str or not lang:
            continue

        try:
            user_hour, user_minute = map(int, time_str.split(":"))
            now_utc = datetime.utcnow()

            user_time = now_utc.replace(hour=user_hour, minute=user_minute, second=0, microsecond=0)
            delta = abs((now_utc - user_time).total_seconds())

            if delta <= 60 and not was_auto_sent(user_id):  # +/-1 минута
                if increment_auto(user_id):  # если не превышен лимит авто
                    content = ask_gpt("Surprise of the day")
                    send_message(user_id, content, TOKEN, keyboard=build_keyboard(lang))
                    mark_auto_sent(user_id)
        except Exception as e:
            print(f"[Scheduler Error] User {user_id}: {e}")


def reset_all_limits():
    reset_limits()
    print("[Scheduler] Daily limits reset.")


def start_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(send_daily_surprises, 'interval', minutes=1)
    scheduler.add_job(reset_all_limits, 'cron', hour=0, minute=0)
    scheduler.start()
    print("[Scheduler] Started")
