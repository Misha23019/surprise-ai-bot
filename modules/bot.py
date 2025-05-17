# modules/bot.py
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

if not TELEGRAM_API_TOKEN:
    raise ValueError("❌ Переменная окружения TELEGRAM_API_TOKEN не установлена!")

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
