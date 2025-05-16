from apscheduler.schedulers.asyncio import AsyncIOScheduler
from modules.database import load_db
from modules.gpt_api import generate_content
from modules.lang import get_text, get_menu
from telegram import Bot
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

async def send_auto_surprises():
    db = load_db()
    for uid, user in db.items():
        try:
            user_time = user.get("time", "10:00")
            now = datetime.now().strftime("%H:%M")
            if now == user_time:
                lang = user.get("lang", "en")
                content = await generate_content("Surprise", lang)
                await bot.send_message(chat_id=uid, text=content)
        except Exception as e:
            print(f"Error sending to {uid}: {e}")

async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_auto_surprises, "cron", minute="0", second="0")  # запускаем каждый час на 00 минут
    scheduler.start()
