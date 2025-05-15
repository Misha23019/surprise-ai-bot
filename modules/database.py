import json
import os

USERS_FILE = "db/users.json"

def ensure_db_dir():
    db_dir = os.path.dirname(USERS_FILE)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

def get_all_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return list(data.keys())
    except (json.JSONDecodeError, IOError) as e:
        # Логируем или игнорируем ошибку, в зависимости от задачи
        print(f"Error reading users file: {e}")
        return []

def save_user(user_id, user_data):
    """
    Добавляет или обновляет пользователя в базе.
    user_data — словарь с данными пользователя.
    """
    ensure_db_dir()
    data = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}

    data[str(user_id)] = user_data
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
