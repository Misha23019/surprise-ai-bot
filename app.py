import os
import logging
from fastapi import FastAPI, Request
from aiogram import types

# ✅ импортируешь готовые bot и dp
from modules.bot import bot, dp
from modules.telegram import setup_handlers


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

# Настроить все хендлеры (если это не делает router)
setup_handlers(dp)

@app.get("/")
async def root():
    return {"status": "Surprise Me! бот працює 🪄"}

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)
    print(f"Webhook встановлено: {WEBHOOK_URL + WEBHOOK_PATH}")

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
