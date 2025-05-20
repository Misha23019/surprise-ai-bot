# modules/scheduler.py

import asyncio
from datetime import datetime
import aiosqlite

from modules.content import generate_scheduled_content
from modules.database import init_db

DB_PATH = "db.sqlite3"
sent_users = set()

async def start_scheduler():
    asyncio.create_task(schedule_loop())

async def schedule_loop():
    global sent_users

    while True:
        now_utc = datetime.utcnow().strftime("%H:%M")

        # Убедимся, что таблица users существует
        try:
            await init_db()
        except Exception as e:
            print(f"Ошибка инициализации базы данных в планировщике: {e}")
            await asyncio.sleep(60)
            continue

        async with aiosqlite.connect(DB_PATH) as db:
            try:
                cursor = await db.execute("SELECT user_id, time, lang FROM users")
                users = await cursor.fetchall()
            except Exception as e:
                print(f"Ошибка чтения пользователей из БД: {e}")
                await asyncio.sleep(60)
                continue

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

# alias для совместимости
schedule_daily_surprise = start_scheduler
