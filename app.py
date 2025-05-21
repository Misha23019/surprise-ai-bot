# surprise-ai-bot/app.py
import os
import logging
import asyncio
from fastapi import FastAPI
from modules.telegram import router as telegram_router
from modules.router import router as main_router
from modules.scheduler import start_scheduler
from modules.limits import init_limits_table
from modules.database import init_db
from modules.bot import bot, dp

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PORT = int(os.getenv("PORT", 8000))
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

app = FastAPI()

# Регистрируем маршруты в диспетчере aiogram
dp.include_router(main_router)
dp.include_router(telegram_router)

@app.on_event("startup")
async def on_startup():
    try:
        await init_db()
        await init_limits_table()
        # Запускаем планировщик (создаёт задачу в текущем event loop)
        loop = asyncio.get_event_loop()
        start_scheduler(loop)
        logging.info("✅ База, лимиты и планировщик инициализированы")
    except Exception as e:
        logging.error(f"❌ Ошибка инициализации: {e}", exc_info=True)

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

async def start_bot():
    logging.info("🚀 Запуск Telegram бота (Long Polling)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import uvicorn

    # Запускаем FastAPI + при необходимости можно отдельно запустить start_bot() в фоне
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level="info")
