from telegram import ReplyKeyboardMarkup
from modules.database import get_user, set_user_lang, set_user_time
from modules.lang import get_text, get_menu, LANGUAGES
from modules.limits import check_limit, register_request
from modules.gpt_api import generate_content

import re

# Установка языка или времени
async def handle_settings(user_id, mode):
    if mode == "lang":
        buttons = [[lang] for lang in LANGUAGES.values()]
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    elif mode == "time":
        return get_text(get_user(user_id)["lang"], "set_time")

# Главный обработчик сообщений
async def handle_message(user_id, text, context):
    user = get_user(user_id)
    lang = user.get("lang", "en")

    # Выбор языка
    for code, name in LANGUAGES.items():
        if text == name:
            set_user_lang(user_id, code)
            await context.bot.send_message(user_id, get_text(code, "set_time"))
            return

    # Установка времени
    if re.match(r"^\d{1,2}:\d{2}$", text):
        set_user_time(user_id, text)
        menu = get_menu(lang)
        await context.bot.send_message(user_id, get_text(lang, "thanks"),
                                       reply_markup=ReplyKeyboardMarkup([menu[i:i+2] for i in range(0, len(menu), 2)], resize_keyboard=True))
        return

    # Контентные кнопки
    if text in get_menu(lang):
        if not check_limit(user_id):
            await context.bot.send_message(user_id, get_text(lang, "limit_reached"))
            return

        register_request(user_id)
        category = text.split(" ")[-1]  # Например: "🎵 Music" → "Music"
        reply = await generate_content(category, lang)
        await context.bot.send_message(user_id, reply)
