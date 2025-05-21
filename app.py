import os
import logging
import asyncio
from fastapi import FastAPI

from modules import (
    init_db,
    init_limits_table,
    start_scheduler
)
from modules.telegram import router as telegram_router
from modules.router import router as main_router
from modules.bot import bot, dp

# --- Логирование ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Конфигурация ---
PORT = int(os.getenv("PORT", 8000))
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

# --- Инициализация FastAPI (только для healthcheck) ---
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Surprise Me! бот працює 🪄"}

@app.get("/healthz")
async def healthcheck():
    return {"status": "ok"}

# --- Регистрация роутеров Aiogram ---
dp.include_router(main_router)
dp.include_router(telegram_router)

# --- Стартовые задачи ---
@app.on_event("startup")
async def on_startup():
    try:
        await init_db()
        logging.info("✅ База данных инициализирована")
    except Exception as e:
        logging.error(f"Ошибка инициализации базы данных: {e}")

    try:
        await init_limits_table()
        logging.info("✅ Таблица лимитов инициализирована")
    except Exception as e:
        logging.error(f"Ошибка инициализации таблицы лимитов: {e}")

    try:
        await start_scheduler()
        logging.info("✅ Планировщик запущен")
    except Exception as e:
        logging.error(f"Ошибка запуска планировщика: {e}")

    asyncio.create_task(dp.start_polling(bot))
    logging.info("🤖 Бот запущен в long polling режиме")
