import os
import json
import datetime
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

from modules.gpt_api import ask_qwen  # твой модуль с запросом к Qwen

from fastapi import FastAPI
from modules.telegram import setup_bot

app = FastAPI()

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
    await message.answer("Привет! У тебя 5 запросов в день к боту.")

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    if not can_use(user_id):
        await message.answer("Извините, лимит на сегодня исчерпан. Приходите завтра!")
        return

    increase(user_id)

@app.get("/")
async def root():
    return {"status": "Bot is running"}

    # Формируем сообщения для GPT
    messages = [
        {"role": "user", "content": message.text}
    ]

    try:
        response_text = ask_qwen(messages)
    except Exception as e:
        await message.answer("Ошибка при запросе к GPT-сервису.")
        return

    await message.answer(response_text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:dp._bot", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
