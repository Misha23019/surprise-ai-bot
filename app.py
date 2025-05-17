import os
import logging
from fastapi import FastAPI, Request
from aiogram import types

from modules import (
    bot, dp, main_router, setup_handlers,  # 👈 добавил
    get_text,
    can_use,
    ask_gpt,
    get_user,
    schedule_daily_surprise,
    send_surprise,
    handle_message,
    default_texts
)

# --- Логирование ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Конфигурация ---
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # например: https://your-domain.onrender.com
PORT = int(os.getenv("PORT", 8000))

# --- Инициализация FastAPI ---
app = FastAPI()

# Настроить все хендлеры
setup_handlers(dp, main_router)

@app.get("/")
async def root():
    return {"status": "Surprise Me! бот працює 🪄"}

@app.on_event("startup")
async def on_startup():
    print(f"✅ ENV: WEBHOOK_URL = {WEBHOOK_URL}")
    print(f"✅ ENV: PORT = {PORT}")
    if not WEBHOOK_URL:
        print("❌ ERROR: WEBHOOK_URL is not set!")
        return

    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)
    print(f"✅ Webhook встановлено: {WEBHOOK_URL + WEBHOOK_PATH}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()

@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
