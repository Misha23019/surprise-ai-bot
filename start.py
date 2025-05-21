# start.py

import os
import asyncio
import logging

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeDefault
from aiogram.fsm.storage.memory import MemoryStorage
from app import app, start_bot  # FastAPI app и функция запуска бота
from modules import main_router  # основной роутер бота

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_DOMAIN = os.getenv("RENDER_EXTERNAL_URL")  # Render предоставляет этот URL
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(main_router)


async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"✅ Webhook установлен: {WEBHOOK_URL}")


async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("🔌 Webhook удалён и бот остановлен")


@app.on_event("startup")
async def startup_event():
    await on_startup()


@app.on_event("shutdown")
async def shutdown_event():
    await on_shutdown()


@app.post(WEBHOOK_PATH)
async def telegram_webhook(update: dict):
    from aiogram.types import Update
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
