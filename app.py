#surprise-ai-bot/app.py
import os
import logging
import asyncio
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PORT = int(os.getenv("PORT", 8000))
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

app = FastAPI()

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

    async def main():
        # Запускаем uvicorn сервер и бота параллельно
        config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
        server = uvicorn.Server(config)

        bot_task = asyncio.create_task(start_bot())
        server_task = asyncio.create_task(server.serve())

        await asyncio.gather(bot_task, server_task)

    asyncio.run(main())
