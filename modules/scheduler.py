from apscheduler.schedulers.asyncio import AsyncIOScheduler
from modules.database import load_db
from modules.gpt_api import generate_content
from datetime import datetime
import logging

scheduler = AsyncIOScheduler()

async def start_scheduler(application):
    scheduler.add_job(send_auto_surprises, "cron", minute="0", second="0", args=[application])
    scheduler.start()
    logging.info("📅 Планировщик запущен")

async def send_auto_surprises(application):
    db = load_db()
    for uid, user in db.items():
        try:
            user_time = user.get("time", "10:00")
            now = datetime.now().strftime("%H:%M")
            if now == user_time:
                lang = user.get("lang", "en")
                content = await generate_content("Surprise", lang)
                await application.bot.send_message(chat_id=uid, text=content)
        except Exception as e:
            logging.warning(f"❌ Ошибка при отправке сюрприза для {uid}: {e}")
