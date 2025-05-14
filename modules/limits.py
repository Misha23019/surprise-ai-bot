import json
import os
from datetime import datetime

LIMITS_FILE = "user_limits.json"
DAILY_LIMIT = 5

def load_limits():
    if os.path.exists(LIMITS_FILE):
        with open(LIMITS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_limits(limits):
    with open(LIMITS_FILE, "w") as f:
        json.dump(limits, f)

def check_limit(chat_id):
    limits = load_limits()
    today = datetime.now().strftime("%Y-%m-%d")
    return limits.get(chat_id, {}).get(today, 0) < DAILY_LIMIT

def increment_limit(chat_id):
    limits = load_limits()
    today = datetime.now().strftime("%Y-%m-%d")
    if chat_id not in limits:
        limits[chat_id] = {}
    limits[chat_id][today] = limits[chat_id].get(today, 0) + 1
    save_limits(limits)
