import json
import os

USERS_FILE = "db/users.json"

def get_all_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return list(data.keys())
