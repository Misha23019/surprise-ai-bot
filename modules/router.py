# modules/router.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from modules.lang import get_text, get_all_languages
from modules.database import get_or_create_user, update_user
from modules.content import generate_surprise, generate_recipe, generate_movie, generate_music, generate_quote, generate_random
from modules.limits import check_daily_limit

# Главное меню
def get_main_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🎁 " + get_text("surprise", lang))],
            [KeyboardButton("🎬 " + get_text("movie", lang)), KeyboardButton("🎵 " + get_text("music", lang))],
            [KeyboardButton("💬 " + get_text("quote", lang)), KeyboardButton("🎲 " + get_text("random", lang))],
            [KeyboardButton("🍳 " + get_text("recipe", lang))],
            [KeyboardButton("⚙ " + get_text("settings", lang))],
        ],
        resize_keyboard=True
    )

# Обработка команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_or_create_user(update.effective_user.id)
    lang = user.get("language")
    
    if not lang:
        # Показываем кнопки выбора языка
        buttons = [
            [InlineKeyboardButton(name, callback_data=f"lang_{code}")]
            for code, name in get_all_languages().items()
        ]
        await update.message.reply_text("🌍 Choose your language:", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        # Если язык уже выбран — показываем меню
        welcome = get_text("welcome", lang)
        await update.message.reply_text(welcome, reply_markup=get_main_menu(lang))

# Обработка callback-кнопок
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    user = get_or_create_user(user_id)

    if data.startswith("lang_"):
        lang_code = data.split("_", 1)[1]
        update_user(user_id, language=lang_code)
        text = get_text("set_lang_success", lang_code)
        await query.edit_message_text(text)
        await context.bot.send_message(chat_id=user_id, text=get_text("set_time_request", lang_code))
    else:
        await context.bot.send_message(chat_id=user_id, text="⚠ Unknown action.")

# Обработка текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    user = get_or_create_user(user_id)
    lang = user.get("language", "en")

    if text.startswith("⚙"):
        # Настройки — повторно предложить язык и время
        buttons = [
            [InlineKeyboardButton(name, callback_data=f"lang_{code}")]
            for code, name in get_all_languages().items()
        ]
        await update.message.reply_text("🌍 Choose your language:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    if ":" in text and len(text) <= 5:
        # Пользователь ввёл время (например, "10:00")
        update_user(user_id, surprise_time=text)
        await update.message.reply_text(get_text("set_time_success", lang), reply_markup=get_main_menu(lang))
        return

    # Проверка лимита
    if not check_daily_limit(user_id):
        await update.message.reply_text(get_text("limit_reached", lang))
        return

    # Основные команды
    if "🎁" in text:
        await update.message.reply_text(generate_surprise(lang))
    elif "🎬" in text:
        await update.message.reply_text(generate_movie(lang))
    elif "🎵" in text:
        await update.message.reply_text(generate_music(lang))
    elif "💬" in text:
        await update.message.reply_text(generate_quote(lang))
    elif "🎲" in text:
        await update.message.reply_text(generate_random(lang))
    elif "🍳" in text:
        await update.message.reply_text(get_text("recipe_request", lang))  # Запросить ингредиенты
    elif "," in text or "и" in text or "and" in text:
        # Предположим, что пользователь ввёл список ингредиентов
        await update.message.reply_text(generate_recipe(text, lang))
    else:
        await update.message.reply_text(get_text("unknown_command", lang))
