from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from modules.lang import get_text, LANGUAGES
from modules.database import add_or_update_user, get_user
from modules.limits import can_send_manual as can_user_request, register_manual_request as increment_manual_count
from modules.telegram import send_message, build_language_keyboard, build_main_menu, build_settings_keyboard

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    add_or_update_user(user_id, language='en')
    send_message(context.bot, user_id, get_text("start", "en"), reply_markup=build_language_keyboard(LANGUAGES))

def language_selection_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    lang_code = query.data.replace("lang_", "")
    if lang_code not in LANGUAGES:
        query.answer("Unsupported language")
        return
    add_or_update_user(user_id, language=lang_code)
    query.answer()
    send_message(context.bot, user_id, get_text("ask_time", lang_code))

def time_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)
    lang = user.get("language", "en") if user else "en"
    time_text = update.message.text.strip()
    import re
    if not re.match(r"^\d{1,2}:\d{2}$", time_text):
        send_message(context.bot, user_id, get_text("invalid_time_format", lang))
        return
    add_or_update_user(user_id, surprise_time=time_text)
    send_message(context.bot, user_id, get_text("time_saved", lang))
    send_message(context.bot, user_id, get_text("choose_action", lang), reply_markup=build_main_menu())

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    user = get_user(user_id)
    lang = user.get("language", "en") if user else "en"

    if data == "surprise":
        if not can_user_request(user_id):
            send_message(context.bot, user_id, get_text("limit_reached", lang))
            query.answer()
            return
        increment_manual_count(user_id)
        send_message(context.bot, user_id, "🎁 Ваш сюрприз...")
    elif data == "settings":
        send_message(context.bot, user_id, "⚙ Налаштування", reply_markup=build_settings_keyboard())
    elif data == "settings_change_language":
        send_message(context.bot, user_id, get_text("choose_language", lang), reply_markup=build_language_keyboard(LANGUAGES))
    elif data == "settings_change_time":
        send_message(context.bot, user_id, get_text("ask_time", lang))
    elif data == "main_menu":
        send_message(context.bot, user_id, get_text("choose_action", lang), reply_markup=build_main_menu())
    else:
        send_message(context.bot, user_id, "Невідома команда.")
    query.answer()

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(language_selection_handler, pattern=r"^lang_"))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, time_handler))
