# modules/telegram.py

import logging
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import aiosqlite

from modules.limits import can_use, increase
from modules.gpt_api import ask_gpt
from modules.bot import bot, dp
from modules.lang import get_text

# --- Настройки ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Переменная окружения BOT_TOKEN не установлена!")
logging.info(f"BOT_TOKEN starts with: {BOT_TOKEN[:4]}***")

router = Router()

# --- Клавиатуры ---
def build_main_keyboard():
    keyboard = [
        [KeyboardButton(text="🎁 Сюрприз"), KeyboardButton(text="🍳 Рецепт")],
        [KeyboardButton(text="🎬 Фільм"), KeyboardButton(text="🎵 Музика")],
        [KeyboardButton(text="💬 Цитата"), KeyboardButton(text="🎲 Рандом")],
        [KeyboardButton(text="⚙ Налаштування")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def build_settings_keyboard():
    keyboard = [
        [KeyboardButton(text="🌐 Змінити мову"), KeyboardButton(text="⏰ Змінити час")],
        [KeyboardButton(text="🔙 Назад до меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- /start ---
@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "👋 Привіт! Щоб отримувати сюрпризи вчасно, скажи мені свій місцевий час у форматі HH:MM (наприклад, 08:30):",
        reply_markup=ReplyKeyboardRemove()
    )

# --- Обработка времени HH:MM ---
@router.message(F.text.regexp(r"^\d{1,2}:\d{2}$"))
async def handle_time_input(message: Message):
    user_id = message.from_user.id

    try:
        local_time = datetime.strptime(message.text.strip(), "%H:%M")
        now_utc = datetime.utcnow()
        now_local = datetime.now()
        local_offset = now_local - now_utc
        time_utc = (local_time - local_offset).time()
        utc_str = time_utc.strftime("%H:%M")

        async with aiosqlite.connect("db.sqlite3") as db:
            await db.execute("UPDATE users SET time = ? WHERE user_id = ?", (utc_str, user_id))
            await db.commit()

        await message.answer("🕒 Час збережено ✅", reply_markup=ReplyKeyboardRemove())
        await message.answer("🎁 Привіт! Як я можу вам допомогти сьогодні?", reply_markup=build_main_keyboard())

    except Exception as e:
        logging.error(f"Помилка при обробці часу: {e}")
        await message.answer("⛔ Некоректний формат часу. Спробуй, наприклад: 09:30")

# --- Обработка кнопок ---
@router.message(F.text == "⚙ Налаштування")
async def open_settings(message: Message):
    await message.answer("⚙ Що ви хочете змінити?", reply_markup=build_settings_keyboard())

@router.message(F.text == "🔙 Назад до меню")
async def back_to_main_menu(message: Message):
    await message.answer("🔙 Повертаю вас у головне меню", reply_markup=build_main_keyboard())

@router.message(F.text == "🌐 Змінити мову")
async def change_language(message: Message):
    await message.answer("🌐 Щоб змінити мову, введіть /start ще раз.")

@router.message(F.text == "⏰ Змінити час")
async def change_time(message: Message):
    await message.answer("⏰ Вкажіть свій новий місцевий час (наприклад, 08:30):", reply_markup=ReplyKeyboardRemove())

# --- GPT-сообщения ---
@router.message(
    F.text & ~F.text.startswith("/") &
    ~F.text.in_([
        "🎁 Сюрприз", "🍳 Рецепт", "🎬 Фільм", "🎵 Музика",
        "💬 Цитата", "🎲 Рандом", "⚙ Налаштування",
        "🌐 Змінити мову", "⏰ Змінити час", "🔙 Назад до меню"
    ]) & ~F.text.regexp(r"^\d{1,2}:\d{2}$")
)
async def handle_gpt(message: Message):
    user_id = message.from_user.id

    if not await can_use(user_id):
        await message.answer("⛔ Вибач, ти вичерпав ліміт на сьогодні.")
        return

    await increase(user_id)
    messages = [{"role": "user", "content": message.text}]
    try:
        response = await ask_gpt(messages)
        await message.answer(response)
    except Exception as e:
        logging.error(f"❌ GPT error: {e}", exc_info=True)
        await message.answer("Сталася помилка при генерації відповіді.")

# --- Запасной хендлер ---
@router.message(F.text)
async def fallback(message: Message):
    await message.answer("🤖 Не впевнений, що ви маєте на увазі. Скористайтеся кнопками або введіть /start.")

# --- Автоматична відправка сюрпризу (для планувальника) ---
async def send_surprise(user_id: int, lang: str = "en"):
    try:
        response = await ask_gpt([{"role": "user", "content": "Surprise me"}], lang=lang)
        await bot.send_message(user_id, response)
    except Exception as e:
        logging.error(f"Помилка при надсиланні автосюрпризу: {e}", exc_info=True)

# --- Ініціалізація хендлерів ---
def setup_handlers(dp: Dispatcher, main_router: Router):
    dp.include_router(main_router)
    dp.include_router(router)

# для сумісності
build_keyboard = build_main_keyboard
