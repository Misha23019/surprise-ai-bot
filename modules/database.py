#modules/database.py
import aiosqlite
from datetime import datetime

DB_PATH = "db.sqlite3"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Проверка: есть ли поле 'limit' — если да, удалим старую таблицу
        try:
            cursor = await db.execute("PRAGMA table_info(users)")
            columns = await cursor.fetchall()
            column_names = [col[1] for col in columns]

            if "limit" in column_names:
                print("⚠️ Обнаружено поле 'limit' — удаляем старую таблицу users...")
                await db.execute("DROP TABLE IF EXISTS users")

        except Exception as e:
            print(f"❌ Ошибка при проверке таблицы users: {e}")

        # Создание таблицы с корректной схемой
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                lang TEXT DEFAULT 'en',
                daily_limit INTEGER DEFAULT 5,
                last_reset TEXT,
                time TEXT
            )
        """)
        await db.commit()

async def get_user(user_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT user_id, lang, daily_limit, last_reset, time FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            return {
                "user_id": row[0],
                "lang": row[1],
                "daily_limit": row[2],
                "last_reset": row[3],
                "time": row[4]
            }
        return None

async def save_user(user_id: str):
    now_str = datetime.utcnow().strftime("%Y-%m-%d")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (user_id, lang, daily_limit, last_reset, time)
            VALUES (?, 'en', 5, ?, NULL)
        """, (user_id, now_str))
        await db.commit()

async def update_user(user_id: str, updates: dict):
    keys = []
    values = []
    for k, v in updates.items():
        keys.append(f"{k} = ?")
        values.append(v)
    values.append(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"""
            UPDATE users SET {', '.join(keys)} WHERE user_id = ?
        """, tuple(values))
        await db.commit()

async def save_language(user_id: str, lang_code: str):
    await update_user(user_id, {"lang": lang_code})

async def get_all_users():
    async with aiosqlite.connect("db.sqlite3") as db:
        cursor = await db.execute("SELECT user_id, time, lang FROM users")
        rows = await cursor.fetchall()
        return rows
        
