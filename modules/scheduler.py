from apscheduler.schedulers.background import BackgroundScheduler
from modules.limits import reset_limits, increment_auto
from modules.telegram import send_message, build_keyboard
from modules.database import get_all_users
from modules.lang import get_user_lang, get_user_time
from modules.router import handle_message
from datetime import datetime, timedelta
import logging
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def send_auto_surprise(chat_id):
    try:
        lang = get_user_lang(chat_id) or 'uk'  # дефолтна мова
        user_time = get_user_time(chat_id)
        if not user_time:
            logging.info(f"User {chat_id} has no set time — skipping auto surprise.")
            return

        # Получаем текущий UTC-время
        now_utc = datetime.utcnow()

        # Парсим время пользователя (строка в формате "HH:MM")
        user_hour, user_minute = map(int, user_time.split(":"))

        # Примерная проверка времени, с допуском +/- 1 минута (чтобы не пропустить)
        if not (now_utc.hour == user_hour and abs(now_utc.minute - user_minute) <= 1):
            return

        # Проверяем лимит на отправку автосюрпризов
        if not increment_auto(chat_id):
            logging.info(f"Автопост для {chat_id} не відправлено: перевищено ліміт.")
            return

        # Получаем ответ от обработчика
        reply = handle_message(chat_id, "/auto_surprise")

        # Отправляем сообщение с клавиатурой
        send_message(chat_id, reply, TELEGRAM_TOKEN, build_keyboard(lang))
        logging.info(f"Автопост для {chat_id} надіслано.")
    except Exception as e:
        logging.error(f"Error sending auto surprise to {chat_id}: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()

    # Сброс лимитов в полночь UTC
    scheduler.add_job(reset_limits, "cron", hour=0, minute=0)

    # Автопосты — запускаем каждую минуту, чтобы не пропустить время пользователя
    scheduler.add_job(
        lambda: [send_auto_surprise(user) for user in get_all_users()],
        "interval", minutes=1
    )

    scheduler.start()
    logging.info("✅ Планувальник запущено")
