# start.py

import os
import logging
import uvicorn
from fastapi import Request

from app import app, bot, dp
from modules.router import router as main_router
from modules.telegram import router as telegram_router

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

WEBHOOK_DOMAIN = os.getenv("RENDER_EXTERNAL_URL")
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup_webhook():
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"✅ Установлен webhook: {WEBHOOK_URL}")


@app.on_event("shutdown")
async def on_shutdown_webhook():
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("🔌 Webhook удалён и бот остановлен")


@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    update = await request.json()
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, log_level="info")
