import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotSettings

import os

# Загрузка токена из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Хранилище состояний (FSM)
storage = MemoryStorage()

# Создаём бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotSettings(parse_mode="HTML"))
dp = Dispatcher(storage=storage)

# Простой обработчик команды /start
@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я Surprise Me! Бот 🎁")

# Фоновая задача запуска бота
async def start_bot():
    print("🚀 Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Главная точка для запуска из FastAPI
def setup_bot():
    asyncio.create_task(start_bot())
