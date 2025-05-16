import json
import os
from datetime import datetime

DB_FILE = "users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

async def get_user(user_id):
    db = load_db()
    return db.get(str(user_id))

async def save_user(user_id):
    db = load_db()
    db[str(user_id)] = {
        "lang": "en",
        "limit": 5,
        "last_reset": str(datetime.utcnow().date()),
        "time": "10:00"
    }
    save_db(db)

async def update_user(user_id, updates: dict):
    db = load_db()
    user = db.get(str(user_id), {})
    user.update(updates)
    db[str(user_id)] = user
    save_db(db)
