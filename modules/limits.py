import json
import datetime
from pathlib import Path
import aiofiles
import asyncio

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

def reset_limits_if_new_day_sync(data):
    today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    for user_id, info in list(data.items()):
        if info.get("date") != today_str:
            data[user_id] = {"count": 0, "date": today_str}

async def can_use(user_id):
    user_id = str(user_id)
    data = await load_limits()
    reset_limits_if_new_day_sync(data)
    info = data.get(user_id, {"count": 0, "date": datetime.datetime.utcnow().strftime("%Y-%m-%d")})
    return info["count"] < LIMIT_PER_DAY

async def increase(user_id):
    user_id = str(user_id)
    data = await load_limits()
    reset_limits_if_new_day_sync(data)
    info = data.get(user_id, {"count": 0, "date": datetime.datetime.utcnow().strftime("%Y-%m-%d")})
    info["count"] += 1
    info["date"] = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    data[user_id] = info
    await save_limits(data)
