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
    """Перевіряє, чи користувач ще має ручні запити"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    data = load_limits()
    user_data = data.get(str(user_id), {})

    if user_data.get("date") != today:
        user_data = {"date": today, "manual_count": 0, "auto_sent": False}

    return user_data["manual_count"] < MAX_REQUESTS_PER_DAY

def increment_manual(user_id):
    """Збільшує лічильник ручних запитів"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    data = load_limits()
    user_data = data.get(str(user_id), {})

    if user_data.get("date") != today:
        user_data = {"date": today, "manual_count": 0, "auto_sent": False}

    user_data["manual_count"] += 1
    data[str(user_id)] = user_data
    save_limits(data)

def was_auto_sent(user_id):
    """Перевіряє, чи було надіслано автоповідомлення сьогодні"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    data = load_limits()
    user_data = data.get(str(user_id), {})
    return user_data.get("date") == today and user_data.get("auto_sent", False)

def mark_auto_sent(user_id):
    """Позначає, що автоповідомлення вже було надіслано"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    data = load_limits()
    user_data = data.get(str(user_id), {})

    if user_data.get("date") != today:
        user_data = {"date": today, "manual_count": 0, "auto_sent": False}

    user_data["auto_sent"] = True
    data[str(user_id)] = user_data
    save_limits(data)

def reset_limits():
    save_limits({})
