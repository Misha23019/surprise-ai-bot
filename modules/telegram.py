from telegram import InlineKeyboardMarkup, InlineKeyboardButton

async def send_message(bot, chat_id, text, reply_markup=None):
    """Отправить сообщение с опциональной клавиатурой."""
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

def build_language_keyboard(languages: dict):
    """Создает inline-клавиатуру выбора языка.
    Пример словаря: {'en': 'English', 'uk': 'Українська'}"""
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"lang_{code}")]
        for code, name in languages.items()
    ]
    return InlineKeyboardMarkup(buttons)

def build_settings_menu():
    """Клавиатура настроек."""
    buttons = [
        [InlineKeyboardButton("🌐 Змінити мову", callback_data="settings_language")],
        [InlineKeyboardButton("⏰ Змінити час", callback_data="settings_time")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(buttons)

def build_main_menu(lang: str = "uk"):
    """Главное меню с кнопками.
    Можно позже добавить локализацию по языку пользователя."""
    buttons = [
        [InlineKeyboardButton("🎁 Сюрприз", callback_data="surprise")],
        [InlineKeyboardButton("⚙ Налаштування", callback_data="settings")]
    ]
    return InlineKeyboardMarkup(buttons)
