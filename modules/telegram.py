# modules/telegram.py
import logging
import os
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import aiosqlite

from modules.limits import can_use, increase
from modules.gpt_api import ask_gpt
from modules.bot import bot, dp
from modules.lang import get_text, save_language
from modules.texts import default_texts
from modules.languages import LANGUAGES  # {'en': 'English', 'uk': 'Українська', ...}


router = Router()
DB_PATH = "db.sqlite3"

async def get_user_lang(user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] else "en"

# --- Клавиатуры с i18n ---
async def build_main_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    lang = await get_user_lang(user_id)
    kb = [
        [KeyboardButton(text=get_text(lang, "surprise_button")), KeyboardButton(text=get_text(lang, "recipe_button"))],
        [KeyboardButton(text=get_text(lang, "movie_button")), KeyboardButton(text=get_text(lang, "music_button"))],
        [KeyboardButton(text=get_text(lang, "quote_button")), KeyboardButton(text=get_text(lang, "random_button"))],
        [KeyboardButton(text=get_text(lang, "settings_button"))]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

async def build_settings_keyboard(user_id: int) -> ReplyKeyboardMarkup:
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
        if not (0 <= local_time.hour < 24 and 0 <= local_time.minute < 60):
            raise ValueError("Invalid time")

        now_utc = datetime.utcnow()
        now_local = datetime.now()
        local_offset = now_local - now_utc
        time_utc = (local_time - local_offset).time()
        utc_str = time_utc.strftime("%H:%M")

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
            await db.execute("UPDATE users SET time = ? WHERE user_id = ?", (utc_str, user_id))
            await db.commit()

        await message.answer(get_text(lang, "time_saved"), reply_markup=ReplyKeyboardRemove())
        kb = await build_main_keyboard(user_id)
        await message.answer(get_text(lang, "menu_message"), reply_markup=kb)
        await refresh_tasks()

    except Exception as e:
        logging.error(f"Error parsing time input from user {user_id}: {e}", exc_info=True)
        await message.answer(get_text(lang, "time_format_error"))

# --- Маппинг для запросов GPT ---
async def map_prompt(text: str, lang: str) -> str:
    prompt_map = {
        get_text(lang, "surprise_button"): "Surprise me",
        get_text(lang, "recipe_button"): "Give me a recipe",
        get_text(lang, "movie_button"): "Recommend a movie",
        get_text(lang, "music_button"): "Suggest music",
        get_text(lang, "quote_button"): "Share a quote",
        get_text(lang, "random_button"): "Random fact",
    }
    return prompt_map.get(text, text)

# --- Обработка кнопок с учетом языка ---
@router.message(F.text)
async def handle_buttons(message: Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    text = message.text

    surprise_btn = get_text(lang, "surprise_button")
    recipe_btn = get_text(lang, "recipe_button")
    movie_btn = get_text(lang, "movie_button")
    music_btn = get_text(lang, "music_button")
    quote_btn = get_text(lang, "quote_button")
    random_btn = get_text(lang, "random_button")
    settings_btn = get_text(lang, "settings_button")
    language_btn = get_text(lang, "language_button")
    time_btn = get_text(lang, "time_button")
    back_btn = get_text(lang, "back_button")

    if text == settings_btn:
        kb = await build_settings_keyboard(user_id)
        await message.answer(get_text(lang, "settings_message"), reply_markup=kb)
    elif text == back_btn:
        kb = await build_main_keyboard(user_id)
        await message.answer(get_text(lang, "back_message"), reply_markup=kb)
    elif text == language_btn:
        from modules.lang import ask_language
        await ask_language(message)
    elif text == time_btn:
        await message.answer(get_text(lang, "ask_time_again"), reply_markup=ReplyKeyboardRemove())
    elif text in {surprise_btn, recipe_btn, movie_btn, music_btn, quote_btn, random_btn}:
        if not await can_use(user_id):
            await message.answer(get_text(lang, "limit_reached"))
            return
        await increase(user_id)
        prompt = await map_prompt(text, lang)
        try:
            response = await ask_gpt([{"role": "user", "content": prompt}], lang=lang)
            await message.answer(response)
        except Exception as e:
            logging.error(f"GPT error for user {user_id}: {e}", exc_info=True)
            await message.answer(get_text(lang, "fallback"))
    else:
        await fallback(message)

# --- Обработка выбора языка ---
@router.message(F.text.in_(list(LANGUAGES.values())))
async def language_selected(message: Message):
    user_id = message.from_user.id
    selected_lang = None
    for code, name in LANGUAGES.items():
        if name.lower().strip() == message.text.lower().strip():
            selected_lang = code
            break
    if selected_lang:
        await save_language(user_id, selected_lang)
        kb = await build_main_keyboard(user_id)
        await message.answer(get_text(selected_lang, "language_chosen"), reply_markup=kb)
    else:
        await message.answer("❌ Language not recognized. Please try again.")

# --- Обработка GPT сообщений (текст без команд, кнопок, времени) ---
@router.message(
    F.text & ~F.text.startswith("/") &
    ~F.text.in_([
        get_text("en", "surprise_button"), get_text("en", "recipe_button"),
        get_text("en", "movie_button"), get_text("en", "music_button"),
        get_text("en", "quote_button"), get_text("en", "random_button"),
        get_text("en", "settings_button"),
        get_text("en", "language_button"), get_text("en", "time_button"),
        get_text("en", "back_button"),
    ]) &
    ~F.text.regexp(r"^\d{1,2}:\d{2}$")
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
        logging.error(f"GPT error for user {user_id}: {e}", exc_info=True)
        await message.answer(get_text(lang, "fallback"))

# --- Запасной хендлер ---
@router.message(F.text)
async def fallback(message: Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(get_text(lang, "fallback"))

# --- Автоматическая отправка сюрприза ---
async def send_surprise(user_id: int):
    try:
        lang = await get_user_lang(user_id)
        response = await ask_gpt([{"role": "user", "content": "Surprise me"}], lang=lang)
        await bot.send_message(user_id, response)
        logging.info(f"Sent surprise to user {user_id}")
    except Exception as e:
        logging.error(f"Ошибка автосюрприза для {user_id}: {e}", exc_info=True)

# --- Регистрация обработчиков ---
def setup_handlers(dp, main_router):
    dp.include_router(main_router)
    dp.include_router(router)

# Для совместимости
build_keyboard = build_main_keyboard
