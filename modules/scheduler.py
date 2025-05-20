import asyncio
from datetime import datetime
from modules.database import load_db
from modules.telegram import bot
from modules.content import generate_scheduled_content

# Для отслеживания, кому уже отправили сюрприз в текущую минуту
sent_users = set()

async def start_scheduler():
    asyncio.create_task(schedule_loop())

async def schedule_loop():
    global sent_users
    while True:
        db = await load_db()  # ✅ исправлено: теперь ждём результат
        now_utc = datetime.utcnow().strftime("%H:%M")
        for user_id, data in db.items():
            user_time = data.get("time", "10:00")
            if now_utc == user_time:
                if user_id not in sent_users:
                    await generate_scheduled_content(user_id, data.get("lang", "en"))
                    sent_users.add(user_id)
            else:
                sent_users.discard(user_id)  # ✅ более безопасно, чем if + remove
        await asyncio.sleep(60)

schedule_daily_surprise = start_scheduler
