from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time, timedelta
import pytz
import logging

from modules.database import get_all_users
from modules.telegram import send_message
from modules.lang import get_text

scheduler = BackgroundScheduler()

def send_daily_surprise():
    users = get_all_users()
    now_utc = datetime.utcnow().time()
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
        
        # Проверяем, совпадает ли текущее UTC-время с 10:00 пользователя
        # Предполагаем, что user_time_str — локальное время пользователя,
        # нам нужно определить, когда наступит 10:00 локального времени в UTC.
        # Но у нас нет часового пояса, только локальное время, поэтому мы сделаем упрощение:
        # Автосюрприз идет если сейчас UTC == 10:00 - user_time + 10:00 ?
        # Вместо этого: сделаем, чтобы функция запускалась каждую минуту и сравнивала, совпадает ли текущее UTC-время
        # с временем пользователя + 10:00? Это сложно без часового пояса.

        # Поэтому пока примем упрощение:
        # Если сейчас UTC время совпадает с user_time_str, отправляем сюрприз

        current_utc_hm = now_utc.hour * 60 + now_utc.minute
        user_hm = user_hour * 60 + user_minute

        # Отправляем сюрприз в 10:00 по местному времени пользователя
        # Значит нужно проверить, что текущее UTC время - user local time = 10:00
        # Без часового пояса это невозможно корректно — нужно сохранять часовой пояс пользователя

        # Для упрощения — если время пользователя == 10:00, отправляем сюрприз
        if user_hour == 10 and now_utc.hour == 10 and now_utc.minute == 0:
            send_surprise(user_id, lang)

def send_surprise(user_id, lang):
    # Здесь можно вызвать content.py для генерации сюрприза
    text = get_text("auto_surprise_text", lang) or "🎁 Ваш автосюрприз!"
    send_message(user_id, text)

def start_scheduler():
    scheduler.add_job(send_daily_surprise, 'interval', minutes=1)
    scheduler.start()
    logging.info("Scheduler started.")
