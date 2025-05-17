# modules/bot.py
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
