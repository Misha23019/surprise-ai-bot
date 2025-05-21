# modules/scheduler.py
import asyncio
import aiosqlite
from datetime import datetime, timedelta
import logging

from modules.telegram import send_surprise

DB_PATH = "db.sqlite3"

async def get_users_to_notify():
    """
    Получаем пользователей с установленным временем автосюрприза (UTC) и языком.
    Возвращает список кортежей: [(user_id, 'HH:MM', lang), ...]
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, time, lang FROM users WHERE time IS NOT NULL") as cursor:
            users = await cursor.fetchall()
    return users

async def wait_until_next_minute():
    """
    Ждем до начала следующей минуты для точного запуска.
    """
    now = datetime.utcnow()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    wait_seconds = (next_minute - now).total_seconds()
    await asyncio.sleep(wait_seconds)

async def scheduler_loop():
    logging.info("⏰ Планировщик автосюрпризов запущен")
    await wait_until_next_minute()

    while True:
        now = datetime.utcnow()
        current_time = now.strftime("%H:%M")

        users = await get_users_to_notify()

        for user_id, utc_time, lang in users:
            if utc_time == current_time:
                try:
                    await send_surprise(user_id, lang or "en")
                    logging.info(f"✅ Отправлен автосюрприз пользователю {user_id} в {current_time} UTC")
                except Exception as e:
                    logging.error(f"Ошибка при отправке автосюрприза пользователю {user_id}: {e}", exc_info=True)

        await asyncio.sleep(60)

def start_scheduler(loop: asyncio.AbstractEventLoop):
    """
    Запуск планировщика в отдельной asyncio-задаче.
    """
    loop.create_task(scheduler_loop())
