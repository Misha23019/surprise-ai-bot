from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot

def send_message(bot: Bot, chat_id, text, reply_markup=None):
    """Отправить сообщение с опциональной клавиатурой."""
    bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, parse_mode='HTML')

def build_language_keyboard(languages: dict):
    """Создает inline-клавиатуру выбора языка."""
    buttons = [
        [InlineKeyboardButton(name, callback_data=f"lang_{code}")]
        for code, name in languages.items()
    ]
    return InlineKeyboardMarkup(buttons)

def build_main_menu():
    """Главное меню."""
    buttons = [
        [InlineKeyboardButton("🎁 Сюрприз", callback_data="surprise")],
        [InlineKeyboardButton("🎬 Фільм", callback_data="film")],
        [InlineKeyboardButton("🎵 Музика", callback_data="music")],
        [InlineKeyboardButton("💬 Цитата", callback_data="quote")],
        [InlineKeyboardButton("🎲 Рандом", callback_data="random")],
        [InlineKeyboardButton("🍳 Рецепт", callback_data="recipe")],
        [InlineKeyboardButton("⚙ Налаштування", callback_data="settings")]
    ]
    return InlineKeyboardMarkup(buttons)

def build_settings_keyboard():
    """Меню настроек."""
    buttons = [
        [InlineKeyboardButton("🌐 Змінити мову", callback_data="settings_change_language")],
        [InlineKeyboardButton("⏰ Змінити час", callback_data="settings_change_time")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(buttons)
