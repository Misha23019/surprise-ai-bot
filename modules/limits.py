import json
import datetime
from pathlib import Path

LIMIT_PER_DAY = 5
DATA_FILE = Path("users_limits.json")

def load_limits():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_limits(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def reset_limits_if_new_day(data):
    today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    for user_id, info in list(data.items()):
        if info.get("date") != today_str:
            data[user_id] = {"count": 0, "date": today_str}

def can_use(user_id):
    data = load_limits()
    reset_limits_if_new_day(data)
    user_id = str(user_id)
    info = data.get(user_id, {"count": 0, "date": datetime.datetime.utcnow().strftime("%Y-%m-%d")})
    return info["count"] < LIMIT_PER_DAY

def increase(user_id):
    data = load_limits()
    reset_limits_if_new_day(data)
    user_id = str(user_id)
    info = data.get(user_id, {"count": 0, "date": datetime.datetime.utcnow().strftime("%Y-%m-%d")})
    info["count"] += 1
    info["date"] = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    data[user_id] = info
    save_limits(data)
