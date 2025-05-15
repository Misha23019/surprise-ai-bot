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

def get_today():
    return datetime.utcnow().strftime("%Y-%m-%d")

def init_user_limits(user_data, today):
    return {"date": today, "manual_count": 0, "auto_count": 0}

def check_limit(user_id):
    today = get_today()
    data = load_limits()
    user_data = data.get(str(user_id))
    if not user_data or user_data.get("date") != today:
        return True
    return user_data.get("manual_count", 0) < MAX_REQUESTS_PER_DAY

def increment_manual(user_id):
    today = get_today()
    data = load_limits()
    user_data = data.get(str(user_id))
    if not user_data or user_data.get("date") != today:
        user_data = init_user_limits(user_data, today)
    user_data["manual_count"] = user_data.get("manual_count", 0) + 1
    data[str(user_id)] = user_data
    save_limits(data)

def was_auto_sent(user_id):
    today = get_today()
    data = load_limits()
    user_data = data.get(str(user_id))
    return user_data is not None and user_data.get("date") == today and user_data.get("auto_count", 0) > 0

def mark_auto_sent(user_id):
    today = get_today()
    data = load_limits()
    user_data = data.get(str(user_id))
    if not user_data or user_data.get("date") != today:
        user_data = init_user_limits(user_data, today)
    user_data["auto_count"] = 1
    data[str(user_id)] = user_data
    save_limits(data)

def reset_limits():
    save_limits({})

def increment_auto(user_id):
    today = get_today()
    data = load_limits()
    user_data = data.get(str(user_id))
    if not user_data or user_data.get("date") != today:
        user_data = init_user_limits(user_data, today)

    total = user_data.get("manual_count", 0) + user_data.get("auto_count", 0)
    if total >= 6:
        return False

    user_data["auto_count"] = user_data.get("auto_count", 0) + 1
    data[str(user_id)] = user_data
    save_limits(data)
    return True
