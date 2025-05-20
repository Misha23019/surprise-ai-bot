# modules/scheduler.py

import asyncio
from datetime import datetime
import aiosqlite
from modules.content import generate_scheduled_content

DB_PATH = "db.sqlite3"
sent_users = set()

async def start_scheduler():
    asyncio.create_task(schedule_loop())

async def schedule_loop():
    global sent_users
    while True:
        now_utc = datetime.utcnow().strftime("%H:%M")

        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT user_id, time, lang FROM users")
            users = await cursor.fetchall()

            for user_id, user_time, lang in users:
                user_time = user_time or "10:00"
                lang = lang or "en"

                if now_utc == user_time:
                    if user_id not in sent_users:
                        await generate_scheduled_content(user_id, lang)
                        sent_users.add(user_id)
                else:
                    sent_users.discard(user_id)

        await asyncio.sleep(60)

schedule_daily_surprise = start_scheduler
