from aiogram import Bot, Dispatcher
import os

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()
