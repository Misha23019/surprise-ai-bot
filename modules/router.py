from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from modules.telegram import (
    send_message,
    build_language_keyboard,
    build_main_menu,
    build_settings_keyboard,
)
from modules.database import add_or_update_user, get_user, increment_manual_count
from modules.lang import get_text

async def start_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    # Добавляем или обновляем пользователя в базе с дефолтным языком и временем
    add_or_update_user(user_id)
    lang = 'en'  # По умолчанию
    text = get_text("welcome_text", lang) or "Welcome! Choose your language:"
    keyboard = build_language_keyboard({
        'en': 'English',
        'uk': 'Українська',
        'ru': 'Русский',
    })
    await send_message(context.bot, user_id, text, reply_markup=keyboard)

async def handle_text(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)
    lang = user['language'] if user else 'en'
    text = update.message.text.strip().lower()

    # Пример простой обработки текстовых команд
    if text in ['settings', '⚙ налаштування', 'настройки']:
        keyboard = build_settings_keyboard()
        text_response = get_text("settings_prompt", lang) or "Настройки:"
        await send_message(context.bot, user_id, text_response, reply_markup=keyboard)
    else:
        # Просто отправим главное меню
        keyboard = build_main_menu(lang)
        text_response = get_text("main_menu_text", lang) or "Главное меню:"
        await send_message(context.bot, user_id, text_response, reply_markup=keyboard)

async def handle_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    user = get_user(user_id)
    lang = user['language'] if user else 'en'

    if data.startswith("set_lang:"):
        new_lang = data.split(":", 1)[1]
        add_or_update_user(user_id, language=new_lang)
        await query.answer(text=get_text("language_changed", new_lang) or "Language changed.")
        # Покажем главное меню на новом языке
        keyboard = build_main_menu(new_lang)
        await send_message(context.bot, user_id, get_text("main_menu_text", new_lang) or "Главное меню:", reply_markup=keyboard)

    elif data == "settings_change_language":
        keyboard = build_language_keyboard({
            'en': 'English',
            'uk': 'Українська',
            'ru': 'Русский',
        })
        await query.answer()
        await send_message(context.bot, user_id, get_text("choose_language", lang) or "Выберите язык:", reply_markup=keyboard)

    elif data == "settings_change_time":
        await query.answer()
        await send_message(context.bot, user_id, get_text("ask_time", lang) or "Введите время сюрприза в формате HH:MM:")

    elif data == "settings":
        keyboard = build_settings_keyboard()
        await query.answer()
        await send_message(context.bot, user_id, get_text("settings_prompt", lang) or "Настройки:", reply_markup=keyboard)

    elif data in ["surprise", "film", "music", "quote", "random", "recipe"]:
        await query.answer()
        # Тут надо реализовать логику показа соответствующего контента
        await send_message(context.bot, user_id, f"{data.capitalize()} выбран. (Функция еще не реализована)")

    else:
        await query.answer()
        await send_message(context.bot, user_id, get_text("unknown_command", lang) or "Неизвестная команда.")

    await query.delete_message()  # опционально удалить сообщение с inline-клавиатурой, если нужно
