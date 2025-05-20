# modules/database.py

import aiosqlite
from datetime import datetime

DB_PATH = "db.sqlite3"

async def init_users_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                lang TEXT DEFAULT 'en',
                time TEXT,
                last_reset TEXT
            )
        """)
        await db.commit()

async def get_user(user_id):
    await init_users_table()
    user_id = str(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT user_id, lang, time, last_reset FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            return {
                "user_id": row[0],
                "lang": row[1],
                "time": row[2],
                "last_reset": row[3],
            }
        return None

async def save_user(user_id):
    await init_users_table()
    user_id = str(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, lang, time, last_reset)
            VALUES (?, 'en', NULL, ?)
        """, (user_id, str(datetime.utcnow().date())))
        await db.commit()

async def update_user(user_id, updates: dict):
    await init_users_table()
    user_id = str(user_id)
    fields = []
    values = []

    for key, value in updates.items():
        fields.append(f"{key} = ?")
        values.append(value)

    values.append(user_id)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"""
            UPDATE users
            SET {", ".join(fields)}
            WHERE user_id = ?
        """, values)
        await db.commit()

async def save_language(user_id, lang_code):
    await update_user(user_id, {"lang": lang_code})
