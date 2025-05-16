import json
import os
from datetime import datetime

DB_FILE = "users.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def init_user(user_id):
    db = load_db()
    uid = str(user_id)
    if uid not in db:
        db[uid] = {
            "lang": "en",
            "time": "10:00",
            "requests": [],
        }
        save_db(db)

def get_user(user_id):
    db = load_db()
    return db.get(str(user_id), {})

def set_user_lang(user_id, lang):
    db = load_db()
    db[str(user_id)]["lang"] = lang
    save_db(db)

def set_user_time(user_id, time_str):
    db = load_db()
    db[str(user_id)]["time"] = time_str
    save_db(db)

def log_request(user_id):
    db = load_db()
    db[str(user_id)]["requests"].append(datetime.utcnow().isoformat())
    save_db(db)

def reset_requests():
    db = load_db()
    for user in db.values():
        user["requests"] = []
    save_db(db)
