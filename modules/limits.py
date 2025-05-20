import json
import datetime
from pathlib import Path
import aiofiles

LIMIT_PER_DAY = 5
DATA_FILE = Path("users_limits.json")

async def load_limits():
    if not DATA_FILE.exists():
        return {}
    async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
        content = await f.read()
        return json.loads(content)

async def save_limits(data):
    async with aiofiles.open(DATA_FILE, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))

def reset_if_new_day(data: dict):
    """Сбрасывает счётчики, если дата устарела."""
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    for user_id in data:
        if data[user_id].get("date") != today:
            data[user_id] = {"count": 0, "date": today}

async def can_use(user_id):
    user_id = str(user_id)
    data = await load_limits()
    reset_if_new_day(data)
    info = data.get(user_id, {"count": 0})
    return info["count"] < LIMIT_PER_DAY

async def increase(user_id):
    user_id = str(user_id)
    data = await load_limits()
    reset_if_new_day(data)
    info = data.get(user_id, {"count": 0})
    info["count"] += 1
    info["date"] = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    data[user_id] = info
    await save_limits(data)

async def reset_limits():
    data = await load_limits()
    reset_if_new_day(data)
    await save_limits(data)
