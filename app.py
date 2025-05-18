import os
import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types

from modules import (
    get_text,
    can_use,
    ask_gpt,
    get_user,
    schedule_daily_surprise,
    send_surprise,
    default_texts
)
from modules.telegram import router as telegram_router, bot as aiogram_bot
from modules.router import router as main_router
from modules.scheduler import start_scheduler

# --- Логирование ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Конфигурация ---
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # например: https://your-domain.onrender.com
PORT = int(os.getenv("PORT", 8000))
TOKEN = os.getenv("BOT_TOKEN")  # Токен бота, должен быть в .env

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

# --- Инициализация бота и диспетчера ---
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

# --- Инициализация FastAPI ---
app = FastAPI()

# --- Регистрация роутеров Aiogram ---
dp.include_router(main_router)      # Основные команды (старт, настройки и т.п.)
dp.include_router(telegram_router)  # GPT-обработчик сообщений

# --- Запуск планировщика (асинхронного) ---
@app.on_event("startup")
async def on_startup():
    if not WEBHOOK_URL:
        logging.error("❌ ERROR: WEBHOOK_URL is not set!")
        return

    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)
    logging.info(f"✅ Webhook установлен: {WEBHOOK_URL + WEBHOOK_PATH}")

    await start_scheduler()
    logging.info("✅ Планировщик запущен")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("✅ Webhook удалён, сессия закрыта")

@app.get("/")
async def root():
    return {"status": "Surprise Me! бот працює 🪄"}

@app.post(WEBHOOK_PATH)
async def handle_webhook(request: Request):
    data = await request.json()
    print("==> Получен апдейт:", data)  # 👈 Добавь это
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get(WEBHOOK_PATH)
@app.head(WEBHOOK_PATH)
async def ping_webhook():
    return {"status": "Webhook is alive"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
