from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def send_message(bot, chat_id, text, reply_markup=None):
    """Отправить сообщение с опциональной клавиатурой."""
    await bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode='HTML')

def build_language_keyboard(languages: dict):
    """Создает inline-клавиатуру выбора языка.
    languages — словарь {code: name}."""
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=name, callback_data=f"set_lang:{code}") for code, name in languages.items()]
    keyboard.add(*buttons)
    return keyboard

def build_settings_keyboard():
    """Клавиатура настроек (⚙ Налаштування)"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("Змінити мову", callback_data="settings_change_language"),
        InlineKeyboardButton("Змінити час", callback_data="settings_change_time"),
    )
    return keyboard

def build_main_menu(lang="en"):
    """Главное меню с кнопками сюрпризов и настроек."""
    # Можно локализовать названия через lang.py, здесь пример на укр:
    buttons = [
        InlineKeyboardButton("🎁 Сюрприз", callback_data="surprise"),
        InlineKeyboardButton("🎬 Фільм", callback_data="film"),
        InlineKeyboardButton("🎵 Музика", callback_data="music"),
        InlineKeyboardButton("💬 Цитата", callback_data="quote"),
        InlineKeyboardButton("🎲 Рандом", callback_data="random"),
        InlineKeyboardButton("🍳 Рецепт", callback_data="recipe"),
        InlineKeyboardButton("⚙ Налаштування", callback_data="settings"),
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
