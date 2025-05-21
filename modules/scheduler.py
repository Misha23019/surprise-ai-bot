# modules/scheduler.py
import logging
import asyncio
import aiosqlite
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()
DB_PATH = "db.sqlite3"

# Импортируем только функцию, чтобы избежать циклического импорта
from modules.telegram import send_surprise

async def send_scheduled_surprises():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, time FROM users WHERE time IS NOT NULL") as cursor:
            async for row in cursor:
                user_id, time_str = row
                try:
                    now = datetime.utcnow()
                    target_time = datetime.strptime(time_str, "%H:%M").time()
                    if now.time().hour == target_time.hour and now.time().minute == target_time.minute:
                        await send_surprise(user_id)
                except Exception as e:
                    logging.error(f"Ошибка при проверке времени для user_id={user_id}: {e}", exc_info=True)

async def refresh_tasks():
    try:
        scheduler.remove_all_jobs()
    except Exception as e:
        logging.warning(f"Не удалось удалить задачи: {e}")

    scheduler.add_job(send_scheduled_surprises, CronTrigger(minute="*"))
    logging.info("✅ Задачи обновлены")

async def start_scheduler():
    scheduler.start()
    await refresh_tasks()
    logging.info("⏰ Планировщик запущен")
