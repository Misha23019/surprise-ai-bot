# modules/telegram.py

import logging
import os
from datetime import datetime, timedelta, time as dt_time
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import aiosqlite

from modules.limits import can_use, increase
from modules.gpt_api import ask_gpt
from modules.bot import bot, dp
from modules.lang import get_text, save_language
from modules.texts import default_texts

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable is missing!")

router = Router()

async def get_user_lang(user_id: int):
    async with aiosqlite.connect("db.sqlite3") as db:
        async with db.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] else "en"

# --- Клавиатуры с i18n ---
async def build_main_keyboard(user_id: int):
    lang = await get_user_lang(user_id)
    kb = [
        [KeyboardButton(text=get_text(lang, "surprise_button")), KeyboardButton(text=get_text(lang, "recipe_button"))],
        [KeyboardButton(text=get_text(lang, "movie_button")), KeyboardButton(text=get_text(lang, "music_button"))],
        [KeyboardButton(text=get_text(lang, "quote_button")), KeyboardButton(text=get_text(lang, "random_button"))],
        [KeyboardButton(text=get_text(lang, "settings_button"))]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

async def build_settings_keyboard(user_id: int):
    lang = await get_user_lang(user_id)
    kb = [
        [KeyboardButton(text=get_text(lang, "language_button")), KeyboardButton(text=get_text(lang, "time_button"))],
        [KeyboardButton(text=get_text(lang, "back_button"))]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- /start ---
@router.message(Command("start"))
async def handle_start(message: Message):
    user_id = message.from_user.id
    # Запрос времени и сброс клавиатуры
    lang = await get_user_lang(user_id)
    text = get_text(lang, "start_choose_time")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())

# --- Обработка времени HH:MM ---
@router.message(F.text.regexp(r"^\d{1,2}:\d{2}$"))
async def handle_time_input(message: Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    try:
        local_time = datetime.strptime(message.text.strip(), "%H:%M")
        now_utc = datetime.utcnow()
        now_local = datetime.now()
        local_offset = now_local - now_utc
        time_utc = (local_time - local_offset).time()
        utc_str = time_utc.strftime("%H:%M")

        async with aiosqlite.connect("db.sqlite3") as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
            await db.execute("UPDATE users SET time = ? WHERE user_id = ?", (utc_str, user_id))
            await db.commit()

        await message.answer(get_text(lang, "time_saved"), reply_markup=ReplyKeyboardRemove())
        await message.answer(get_text(lang, "menu_message"), reply_markup=await build_main_keyboard(user_id))

    except Exception as e:
        logging.error(f"Error parsing time: {e}")
        await message.answer(get_text(lang, "time_format_error"))

# --- Обработка кнопок ---
@router.message(F.text == "⚙ Налаштування")
async def open_settings(message: Message):
    user_id = message.from_user.id
    kb = await build_settings_keyboard(user_id)
    lang = await get_user_lang(user_id)
    await message.answer(get_text(lang, "settings_message"), reply_markup=kb)

@router.message(F.text == "🔙 Назад до меню")
async def back_to_main_menu(message: Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    kb = await build_main_keyboard(user_id)
    await message.answer(get_text(lang, "back_message"), reply_markup=kb)

@router.message(F.text == "🌐 Змінити мову")
async def change_language(message: Message):
    user_id = message.from_user.id
    # Предлагаем выбрать язык
    from modules.lang import ask_language
    await ask_language(message)

@router.message(F.text == "⏰ Змінити час")
async def change_time(message: Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    await message.answer(get_text(lang, "ask_time_again"), reply_markup=ReplyKeyboardRemove())

# --- Обработка выбора языка ---

@router.message(F.text.in_(list(default_texts["en"].values())))  # Можно заменить на более точный фильтр или ручную проверку
async def language_selected(message: Message):
    user_id = message.from_user.id
    # Найдём код языка по названию из клавиатуры
    from modules.languages import LANGUAGES  # {'en': 'English', 'uk': 'Українська', ...}
    selected_lang = None
    for code, name in LANGUAGES.items():
        if name == message.text:
            selected_lang = code
            break
    if selected_lang:
        await save_language(user_id, selected_lang)
        lang = await get_user_lang(user_id)
        await message.answer(get_text(lang, "language_chosen"), reply_markup=await build_main_keyboard(user_id))
    else:
        await message.answer("❌ Language not recognized. Please try again.")

# --- GPT-сообщения ---
@router.message(
    F.text & ~F.text.startswith("/") &
    ~F.text.in_([
        # Все кнопки на разных языках лучше взять из словаря, но для простоты:
        "🎁 Сюрприз", "🍳 Рецепт", "🎬 Фільм", "🎵 Музика",
        "💬 Цитата", "🎲 Рандом", "⚙ Налаштування",
        "🌐 Змінити мову", "⏰ Змінити час", "🔙 Назад до меню"
    ]) & ~F.text.regexp(r"^\d{1,2}:\d{2}$")
)
async def handle_gpt(message: Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)

    if not await can_use(user_id):
        await message.answer(get_text(lang, "limit_reached"))
        return

    await increase(user_id)
    messages = [{"role": "user", "content": message.text}]
    try:
        response = await ask_gpt(messages, lang=lang)
        await message.answer(response)
    except Exception as e:
        logging.error(f"GPT error: {e}", exc_info=True)
        await message.answer(get_text(lang, "fallback"))

# --- Запасной хендлер ---
@router.message(F.text)
async def fallback(message: Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(get_text(lang, "fallback"))

# --- Автоматическая отправка сюрприза ---
async def send_surprise(user_id: int, lang: str = "en"):
    try:
        response = await ask_gpt([{"role": "user", "content": "Surprise me"}], lang=lang)
        await bot.send_message(user_id, response)
    except Exception as e:
        logging.error(f"Ошибка автосюрприза: {e}", exc_info=True)

# --- Планировщик автосюрпризов в 10:00 по локальному времени пользователя ---

async def send_daily_surprises():
    async with aiosqlite.connect("db.sqlite3") as db:
        now_utc = datetime.utcnow()
        now_str = now_utc.strftime("%H:%M")
        # Найдем пользователей, у которых время совпадает с текущим UTC-часом и минутой
        async with db.execute("SELECT user_id, lang FROM users WHERE time = ?", (now_str,)) as cursor:
            rows = await cursor.fetchall()
            for user_id, lang in rows:
                await send_surprise(user_id, lang=lang if lang else "en")

# --- Регистрация обработчиков ---
def setup_handlers(dp: Dispatcher, main_router: Router):
    dp.include_router(main_router)
    dp.include_router(router)

# Для совместимости
build_keyboard = build_main_keyboard
