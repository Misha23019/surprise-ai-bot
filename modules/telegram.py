# modules/telegram.py
# modules/telegram.py
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from modules.limits import can_use, increase
from modules.gpt_api import ask_gpt
import os

# --- Настройки Telegram ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Переменная окружения BOT_TOKEN не установлена!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Роутер для GPT-сообщений ---
router = Router()

@router.message(F.text & ~F.text.startswith("/"))
async def handle_message(message: Message):
    user_id = message.from_user.id
    if not await can_use(user_id):  # await обязательно
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

# --- Подключение всех роутеров ---
def setup_handlers(dp: Dispatcher, main_router: Router):
    dp.include_router(main_router)  # основной роутер
    dp.include_router(router)       # GPT-обработчик
