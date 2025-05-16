# modules/bot.py
import os
from aiogram import Bot, Dispatcher

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()
