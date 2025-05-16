from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from modules.lang import get_text, LANGUAGES
from modules.database import add_or_update_user, get_user
from modules.limits import can_user_request, increment_manual_count
from modules.telegram import send_message, build_language_keyboard, build_main_menu, build_settings_menu
import re

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_or_update_user(user_id, language='en')
    await send_message(user_id, get_text("start", "en"), reply_markup=build_language_keyboard(LANGUAGES))

# Выбор языка
async def language_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    lang_code = query.data.replace("lang_", "")
    if lang_code not in LANGUAGES:
        await query.answer("Unsupported language")
        return
    add_or_update_user(user_id, language=lang_code)
    await query.answer()
    await send_message(user_id, get_text("ask_time", lang_code))

# Ввод времени
async def time_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    lang = user.get("language", "en") if user else "en"
    time_text = update.message.text.strip()

    if not re.match(r"^\d{1,2}:\d{2}$", time_text):
        await send_message(user_id, get_text("invalid_time_format", lang))
        return

    add_or_update_user(user_id, surprise_time=time_text)
    await send_message(user_id, get_text("time_saved", lang))
    await send_message(user_id, get_text("choose_action", lang), reply_markup=build_main_menu())

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    user = get_user(user_id)
    lang = user.get("language", "en") if user else "en"

    if data == "surprise":
        if not can_user_request(user_id):
            await send_message(user_id, get_text("limit_reached", lang))
            await query.answer()
            return
        increment_manual_count(user_id)
        await send_message(user_id, "🎁 Ваш сюрприз...")  # Тут вставить генерацию сюрприза
    elif data == "settings":
        await send_message(user_id, "⚙ Налаштування", reply_markup=build_settings_menu())
    elif data == "settings_language":
        await send_message(user_id, get_text("choose_language", lang), reply_markup=build_language_keyboard(LANGUAGES))
    elif data == "settings_time":
        await send_message(user_id, get_text("ask_time", lang))
    elif data == "main_menu":
        await send_message(user_id, get_text("choose_action", lang), reply_markup=build_main_menu())
    else:
        await send_message(user_id, "Невідома команда.")

    await query.answer()

# Регистрация хендлеров
def register_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_selection_handler, pattern=r"^lang_"))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, time_handler))
