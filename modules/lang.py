from aiogram import types
from modules.database import update_user
from modules.texts import LANGUAGES, TEXTS

FLAGS = {
    "en": "🇬🇧",
    "ua": "🇺🇦",
    "ru": "🇷🇺",
    "es": "🇪🇸",
    "fr": "🇫🇷",
    "de": "🇩🇪",
    "it": "🇮🇹",
    "pl": "🇵🇱",
    "tr": "🇹🇷",
    "pt": "🇵🇹",
    "zh": "🇨🇳",
    "ja": "🇯🇵",
    "ko": "🇰🇷",
    "hi": "🇮🇳",
    "ar": "🇸🇦"
}

def get_flag(lang_code):
    return FLAGS.get(lang_code, "🏳️")

async def ask_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=f"{get_flag(code)} {name}")] for code, name in LANGUAGES.items()
        ],
        resize_keyboard=True
    )
    await message.answer("Оберiть мову / Choose language:", reply_markup=keyboard)

async def ask_time(message: types.Message):
    await message.answer("Вкажiть свiй мiсцевий час (наприклад, 15:30) – це потрiбно, щоб надсилати сюрприз о 10:00 вашого часу.")

def get_text(lang, key, default=None):
    return TEXTS.get(lang, TEXTS["en"]).get(key, default if default is not None else key)

async def save_language(user_id, lang_code):
    await update_user(user_id, {"lang": lang_code})
