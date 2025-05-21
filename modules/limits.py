# modules/limits.py
import aiosqlite
from datetime import datetime

LIMIT_PER_DAY = 5
DB_PATH = "db.sqlite3"

async def init_limits_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS limits (
                user_id TEXT PRIMARY KEY,
                count INTEGER,
                date TEXT
            )
        """)
        await db.commit()

async def can_use(user_id: str) -> bool:
    user_id = str(user_id)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT count, date FROM limits WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()

        # Если записи нет или дата устарела — можно использовать
        if row is None or row[1] != today:
            return True

        # Проверяем, не превышен ли лимит
        return row[0] < LIMIT_PER_DAY

async def increase(user_id: str):
    user_id = str(user_id)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT count, date FROM limits WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()

        if row is None or row[1] != today:
            count = 1
        else:
            count = row[0] + 1

        await db.execute("""
            INSERT INTO limits (user_id, count, date)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET count = excluded.count, date = excluded.date
        """, (user_id, count, today))
        await db.commit()

async def reset_limits():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE limits SET count = 0, date = ?", (today,))
        await db.commit()
