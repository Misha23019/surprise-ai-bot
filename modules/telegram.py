# modules/telegram.py
import logging
import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from modules.limits import can_use, increase
from modules.gpt_api import ask_gpt

logging.basicConfig(level=logging.INFO)

# --- Настройки Telegram ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Переменная окружения BOT_TOKEN не установлена!")

logging.info(f"BOT_TOKEN starts with: {BOT_TOKEN[:4]}***")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Роутер для GPT-сообщений ---
router = Router()

@router.message(F.text & ~F.text.startswith("/"))
async def handle_message(message: Message):
    user_id = message.from_user.id
    if not await can_use(user_id):
        await message.answer("Извините, лимит на сегодня исчерпан.")
        return

    await increase(user_id)

    messages = [{"role": "user", "content": message.text}]
    try:
        response = await ask_gpt(messages)
        await message.answer(response)
    except Exception as e:
        logging.error(f"Ошибка при обращении к GPT: {e}", exc_info=True)
        await message.answer("Произошла ошибка при обращении к GPT")

# --- Отправка сюрприза (используется в scheduler) ---
async def send_surprise(user_id: int, lang: str = "en"):
    try:
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
