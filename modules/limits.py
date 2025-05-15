import json
import os
from datetime import datetime

LIMITS_FILE = "data/limits.json"
MAX_REQUESTS_PER_DAY = 5

def load_limits():
    if os.path.exists(LIMITS_FILE):
        with open(LIMITS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_limits(data):
    os.makedirs(os.path.dirname(LIMITS_FILE), exist_ok=True)
    with open(LIMITS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def check_limit(user_id):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    data = load_limits()
    user_data = data.get(str(user_id), {})

    if user_data.get("date") != today:
        user_data = {"date": today, "count": 0}

    if user_data["count"] >= MAX_REQUESTS_PER_DAY:
        return False

    user_data["count"] += 1
    data[str(user_id)] = user_data
    save_limits(data)
    return True

def reset_limits():
    # Можешь вызывать по расписанию, если хочешь вручную
    save_limits({})
