import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from modules.bot import bot, dp
from modules.telegram import setup_handlers

# --- Конфигурация ---
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Полный адрес, например: https://your-domain.com
PORT = int(os.getenv("PORT", 8000))

# --- Инициализация ---
app = FastAPI()

# Настроить все хендлеры
setup_handlers(dp)

@app.get("/")
async def root():
    return {"status": "Surprise Me! бот работает 🪄"}

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)
    print(f"Webhook установлен: {WEBHOOK_URL + WEBHOOK_PATH}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()

# --- Интеграция webhook с FastAPI ---
@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(update)
    return {"status": "ok"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    update = types.Update(**await request.json())
    await dp.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Hello, world!"}


# --- Запуск локально ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
