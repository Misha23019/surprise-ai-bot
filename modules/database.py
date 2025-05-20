import json
import os
from datetime import datetime
import aiofiles

DB_FILE = "users.json"

async def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    async with aiofiles.open(DB_FILE, "r") as f:
        content = await f.read()
        return json.loads(content)

async def save_db(data):
    async with aiofiles.open(DB_FILE, "w") as f:
        await f.write(json.dumps(data, indent=2))

async def get_user(user_id):
    db = await load_db()
    return db.get(str(user_id))

async def save_user(user_id):
    db = await load_db()
    db[str(user_id)] = {
        "lang": "en",
        "limit": 5,
        "last_reset": str(datetime.utcnow().date()),
        "time": None  # пусть сначала сам введёт
    }
    await save_db(db)

async def update_user(user_id, updates: dict):
    db = await load_db()
    user = db.get(str(user_id), {})
    user.update(updates)
    db[str(user_id)] = user
    await save_db(db)

async def save_language(user_id, lang_code):
    await update_user(user_id, {"lang": lang_code})
