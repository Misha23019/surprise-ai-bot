# modules/scheduler.py
import logging
from datetime import datetime, time
import aiosqlite
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from modules.bot import bot
from modules.gpt_api import ask_gpt
from modules.telegram import get_user_lang
import modules.shared as shared

DB_PATH = "db.sqlite3"
scheduler = AsyncIOScheduler()
_refresh_callback = None  # Локальная переменная

def register_refresh_callback(callback):
    """
    Принимает ссылку на функцию refresh_tasks из telegram.py
    и сохраняет в shared и локально.
    """
    global _refresh_callback
    shared.refresh_tasks = callback
    _refresh_callback = callback

async def send_scheduled_surprise(user_id: int):
    try:
        lang = await get_user_lang(user_id)
        response = await ask_gpt([{"role": "user", "content": "Surprise me"}], lang=lang)
        await bot.send_message(user_id, response)
        logging.info(f"✅ Sent scheduled surprise to user {user_id}")
    except Exception as e:
        logging.error(f"❌ Error sending surprise to user {user_id}: {e}", exc_info=True)

def schedule_user_task(user_id: int, hour: int, minute: int):
    """
    Добавляет задачу для отправки сюрприза конкретному пользователю.
    """
    trigger = CronTrigger(hour=hour, minute=minute)
    job_id = f"user_{user_id}"
    scheduler.add_job(send_scheduled_surprise, trigger, args=[user_id], id=job_id, replace_existing=True)

async def refresh_tasks():
    """
    Перечитывает всех пользователей из базы и пересоздаёт задачи.
    """
    scheduler.remove_all_jobs()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id, time FROM users WHERE time IS NOT NULL") as cursor:
            async for row in cursor:
                user_id, time_str = row
                try:
                    t = datetime.strptime(time_str, "%H:%M").time()
                    schedule_user_task(user_id, t.hour, t.minute)
                    logging.info(f"✅ Scheduled surprise for user {user_id} at {t}")
                except Exception as e:
                    logging.error(f"❌ Failed to schedule user {user_id}: {e}", exc_info=True)

async def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logging.info("🕒 Scheduler started.")
    if _refresh_callback:
        await _refresh_callback()  # можно использовать shared.refresh_tasks()
