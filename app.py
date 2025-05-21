#surprise-ai-bot/app.py
import os
import logging
from fastapi import FastAPI

from modules import (
    get_text,
    can_use,
    ask_gpt,
    get_user,
    schedule_daily_surprise,
    send_surprise,
    default_texts
)
from modules.telegram import router as telegram_router
from modules.router import router as main_router
from modules.scheduler import start_scheduler
from modules.limits import init_limits_table
from modules.database import init_db
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

# --- Инициализация FastAPI ---
app = FastAPI()

# --- Роутеры Aiogram ---
dp.include_router(main_router)
dp.include_router(telegram_router)

@app.on_event("startup")
async def on_startup():
    try:
        await init_db()
        await init_limits_table()
        await start_scheduler()
        logging.info("✅ База, лимиты и планировщик инициализированы")
    except Exception as e:
        logging.error(f"❌ Ошибка инициализации: {e}")

    # Запуск Long Polling
    import asyncio
    asyncio.create_task(dp.start_polling(bot))
    logging.info("🚀 Бот запущен в режиме Long Polling")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    logging.info("🔌 Сессия Telegram бота закрыта")

@app.get("/")
async def root():
    return {"status": "Surprise Me! бот працює 🪄"}

@app.get("/healthz")
async def healthcheck():
    return {"status": "ok"}
