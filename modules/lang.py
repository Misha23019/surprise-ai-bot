from aiogram import types
from modules.database import update_user
from modules.texts import LANGUAGES, TEXTS

async def ask_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=lang)] for lang in LANGUAGES.values()
        ],
        resize_keyboard=True
    )
    await message.answer("Оберіть мову / Choose language:", reply_markup=keyboard)

async def ask_time(message: types.Message):
    await message.answer("Вкажіть свій місцевий час (наприклад, 15:30) – це потрібно, щоб надсилати сюрприз о 10:00 вашого часу.")

def get_text(lang, key, default=None):
    return TEXTS.get(lang, TEXTS["en"]).get(key, default if default is not None else key)

async def save_language(user_id, lang_code):
    await update_user(user_id, {"lang": lang_code})

def get_all_languages():
    return LANGUAGES
