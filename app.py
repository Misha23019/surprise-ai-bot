import json
import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

import asyncio
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

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

@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await message.answer("Привет! Это бот с лимитом 5 запросов в день.")

@dp.message()
async def echo_handler(message: Message):
    user_id = message.from_user.id
    if not can_use(user_id):
        await message.answer("Извините, лимит на сегодня исчерпан. Приходите завтра!")
        return
    increase(user_id)

    # Здесь логика бота, например эхо:
    await message.answer(f"Ваш запрос принят. Использовано {load_limits()[str(user_id)]['count']} из {LIMIT_PER_DAY} запросов сегодня.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:dp._bot", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
