import asyncio
from datetime import datetime
from modules.database import load_db
from modules.bot import bot
from modules.content import generate_scheduled_content

async def start_scheduler():
    asyncio.create_task(schedule_loop())

async def schedule_loop():
    while True:
        db = load_db()
        for user_id, data in db.items():
            now_utc = datetime.utcnow().strftime("%H:%M")
            user_time = data.get("time", "10:00")
            if now_utc == user_time:
                await generate_scheduled_content(user_id, data["lang"])
        await asyncio.sleep(60)
