from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from modules.lang import get_text, get_languages

async def send_message(bot, chat_id, text, reply_markup=None):
    """
    Відправляє повідомлення з необов'язковою inline-клавіатурою.
    """
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

def build_language_keyboard():
    """
    Створює клавіатуру вибору мови на основі get_languages().
    """
    languages = get_languages()
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"lang_{code}")]
        for code, name in languages.items()
    ]
    return InlineKeyboardMarkup(buttons)

def build_main_menu(lang: str = "en"):
    """
    Головне меню з локалізованими кнопками.
    """
    buttons = [
        [InlineKeyboardButton(get_text("surprise_btn", lang), callback_data="surprise")],
        [InlineKeyboardButton(get_text("settings_btn", lang), callback_data="settings")]
    ]
    return InlineKeyboardMarkup(buttons)

def build_settings_menu(lang: str = "en"):
    """
    Меню налаштувань з локалізованими кнопками.
    """
    buttons = [
        [InlineKeyboardButton(get_text("change_language", lang), callback_data="settings_language")],
        [InlineKeyboardButton(get_text("change_time", lang), callback_data="settings_time")],
        [InlineKeyboardButton(get_text("back", lang), callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(buttons)
