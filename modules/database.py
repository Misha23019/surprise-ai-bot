import sqlite3
import threading
from contextlib import closing

DB_PATH = "surprise_me.db"
lock = threading.Lock()

def init_db():
    with lock, sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'en',
                surprise_time TEXT,
                manual_count INTEGER DEFAULT 0,
                last_request_date TEXT
            )
        """)
        conn.commit()

def add_or_update_user(user_id, language=None, surprise_time=None):
    with lock, sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        exists = c.fetchone()
        if exists:
            if language is not None:
                c.execute("UPDATE users SET language=? WHERE user_id=?", (language, user_id))
            if surprise_time is not None:
                c.execute("UPDATE users SET surprise_time=? WHERE user_id=?", (surprise_time, user_id))
        else:
            c.execute(
                "INSERT INTO users (user_id, language, surprise_time) VALUES (?, ?, ?)",
                (user_id, language or 'en', surprise_time, timezone or 'UTC')
            )
        conn.commit()

def get_user(user_id):
    with lock, sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, language, surprise_time, timezone, manual_count, last_request_date FROM users WHERE user_id=?", (user_id,))
        row = c.fetchone()
        if row:
            return {
                "user_id": row[0],
                "language": row[1],
                "surprise_time": row[2],
                "timezone": row[3] or 'UTC',
                "manual_count": row[4],
                "last_request_date": row[5]
            }
        return None

def get_all_users():
    with lock, sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, language, surprise_time, timezone, manual_count, last_request_date FROM users")
        rows = c.fetchall()
        users = []
        for row in rows:
            users.append({
                "user_id": row[0],
                "language": row[1],
                "surprise_time": row[2],
                "timezone": row[3] or 'UTC',
                "manual_count": row[4],
                "last_request_date": row[5]
            })
        return users


def reset_manual_counts_if_needed():
    from datetime import datetime
    today = datetime.utcnow().strftime("%Y-%m-%d")
    with lock, sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, last_request_date FROM users")
        users = c.fetchall()
        for user_id, last_date in users:
            if last_date != today:
                c.execute(
                    "UPDATE users SET manual_count=0, last_request_date=? WHERE user_id=?",
                    (today, user_id)
                )
        conn.commit()

def increment_manual_count(user_id):
    from datetime import datetime
    today = datetime.utcnow().strftime("%Y-%m-%d")
    with lock, sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        user = get_user(user_id)
        if user:
            # Сброс, если дата изменилась
            if user['last_request_date'] != today:
                c.execute(
                    "UPDATE users SET manual_count=1, last_request_date=? WHERE user_id=?",
                    (today, user_id)
                )
            else:
                c.execute(
                    "UPDATE users SET manual_count=manual_count+1 WHERE user_id=?",
                    (user_id,)
                )
            conn.commit()

def get_all_users():
    with lock, sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT user_id, language, surprise_time, manual_count, last_request_date FROM users")
        rows = c.fetchall()
        users = []
        for row in rows:
            users.append({
                "user_id": row[0],
                "language": row[1],
                "surprise_time": row[2],
                "manual_count": row[3],
                "last_request_date": row[4]
            })
        return users
