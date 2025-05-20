# modules/scheduler.py

import asyncio
from datetime import datetime
import aiosqlite
import logging

from modules.content import generate_scheduled_content
from modules.database import init_db, get_all_users

DB_PATH = "db.sqlite3"
sent_users = set()

async def start_scheduler():
    logging.info("⏰ Планировщик запущен")
    while True:
        now_utc = datetime.utcnow().time().strftime("%H:%M")
        async with aiosqlite.connect("db.sqlite3") as db:
            async with db.execute("SELECT user_id, time, lang FROM users") as cursor:
                async for user_id, time_str, lang in cursor:
                    if time_str == now_utc:
                        try:
                            await send_surprise(user_id, lang or "en")
                            logging.info(f"✅ Отправлен сюрприз пользователю {user_id} в {now_utc} UTC")
                        except Exception as e:
                            logging.error(f"Ошибка при отправке сюрприза пользователю {user_id}: {e}")
        await asyncio.sleep(60)

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
