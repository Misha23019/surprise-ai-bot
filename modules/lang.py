from aiogram import types
from modules.database import update_user
from modules.texts import LANGUAGES, TEXTS

async def ask_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lang in LANGUAGES.values():
        keyboard.add(types.KeyboardButton(text=lang))
    await message.answer("Оберіть мову / Choose language:", reply_markup=keyboard)

async def ask_time(message: types.Message):
    await message.answer("Вкажіть свій місцевий час (наприклад, 15:30) – це потрібно, щоб надсилати сюрприз о 10:00 вашого часу.")

def get_text(lang, key):
    return TEXTS.get(lang, TEXTS["en"]).get(key, key)

async def save_language(user_id, lang_code):
    await update_user(user_id, {"lang": lang_code})
