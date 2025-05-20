# modules/telegram.py
import logging
import os
from datetime import datetime, timedelta
import aiosqlite

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from modules.limits import can_use, increase
from modules.gpt_api import ask_gpt
from modules.bot import bot, dp
from modules.lang import get_text
from modules.database import DB_PATH

logging.basicConfig(level=logging.INFO)

# --- Настройки Telegram ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Переменная окружения BOT_TOKEN не установлена!")

logging.info(f"BOT_TOKEN starts with: {BOT_TOKEN[:4]}***")

# --- Роутер для GPT-сообщений ---
router = Router()

@router.message(F.text & ~F.text.startswith("/"))
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    # Попытка распознать время (например, 09:30)
    try:
        local_time = datetime.strptime(text, "%H:%M").time()
        now_local = datetime.now()
        now_utc = datetime.utcnow()

        # Смещение между локальным временем и UTC
        offset_minutes = int((now_local - now_utc).total_seconds() / 60)

        # Конвертируем введённое пользователем время (10:00) в UTC
        local_dt = datetime.combine(datetime.today(), local_time)
        utc_dt = local_dt - timedelta(minutes=offset_minutes)
        utc_time_str = utc_dt.strftime("%H:%M")

        user_id = message.from_user.id
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("UPDATE users SET time = ? WHERE user_id = ?", (utc_time_str, user_id))
            await db.commit()

        await message.answer(get_text("time_saved", user_id))
        await message.answer(get_text("menu_greeting", user_id), reply_markup=build_keyboard())
        return
    except ValueError:
        pass  # Не время — продолжаем как обычное GPT-сообщение

    if not await can_use(user_id):
        await message.answer("Извините, лимит на сегодня исчерпан.")
        return

    await increase(user_id)

    messages = [{"role": "user", "content": text}]
    try:
        response = await ask_gpt(messages)
        await message.answer(response)
    except Exception as e:
        logging.error(f"Ошибка при обращении к GPT: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обращении к GPT")

# --- Отправка сюрприза (используется в scheduler) ---
async def send_surprise(user_id: int, lang: str = "en"):
    try:
        bot = get_bot()
        response = await ask_gpt([{"role": "user", "content": "Surprise me"}], lang=lang)
        await bot.send_message(user_id, response)
    except Exception as e:
        logging.error(f"Ошибка при отправке автосюрприза: {e}", exc_info=True)

# --- Генерация клавиатуры (по необходимости) ---
def build_keyboard():
    keyboard = [
        [KeyboardButton(text="🎁 Сюрприз"), KeyboardButton(text="🍳 Рецепт")],
        [KeyboardButton(text="🎬 Фільм"), KeyboardButton(text="🎵 Музика")],
        [KeyboardButton(text="💬 Цитата"), KeyboardButton(text="🎲 Рандом")],
        [KeyboardButton(text="⚙ Налаштування")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- Подключение всех роутеров ---
def setup_handlers(dp: Dispatcher, main_router: Router):
    dp.include_router(main_router)
    dp.include_router(router)

@router.message(F.text)
async def debug_all(message: Message):
    print("Получено сообщение:", message.text)
    await message.answer("Отладка: сообщение получено.")
