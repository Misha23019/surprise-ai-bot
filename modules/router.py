#surprise-ai-bot/modules/router.py
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from modules.lang import get_text, ask_language, ask_time, LANGUAGES
from modules.limits import can_use, increase
from modules.content import generate_content_from_message, generate_content_from_text
from modules.database import get_user, save_user, save_language, update_user
import re

router = Router()

def main_menu(lang: str) -> types.ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру с основными кнопками меню,
    локализованными на выбранном языке.
    """
    buttons = [
        ["🎁 " + get_text(lang, "surprise")],
        ["🎬 " + get_text(lang, "movie"), "🎵 " + get_text(lang, "music")],
        ["💬 " + get_text(lang, "quote"), "🎲 " + get_text(lang, "random")],
        ["🍳 " + get_text(lang, "recipe")],
        [get_text(lang, "settings") + " ⚙"]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=btn) for btn in row] for row in buttons],
        resize_keyboard=True
    )
    return keyboard

@router.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    if not user:
        await save_user(user_id)
        await ask_language(message)
    else:
        lang = user.get("lang") or "en"
        await message.answer(get_text(lang, 'menu'), reply_markup=main_menu(lang))

@router.message(F.text.lower().in_({"налаштування", "⚙ налаштування", "settings", "⚙ settings"}))
async def settings_handler(message: types.Message):
    # Пользователь запросил настройки — предложить выбор языка
    await ask_language(message)

@router.message(F.text.lower().in_({
    "привіт", "hello", "🎁 сюрприз", "🎬 фільм", "🎵 музика", "💬 цитата", "🎲 рандом", "🍳 рецепт"
}))
async def content_request(message: types.Message):
    user_id = message.from_user.id
    if not await can_use(user_id):
        lang = (await get_user(user_id)).get("lang", "en")
        await message.answer(get_text(lang, "limit_reached", "Ви досягли ліміту на сьогодні. Спробуйте завтра 🙏"))
        return

    # Увеличиваем счетчик запросов
    await increase(user_id)
    await generate_content_from_message(message)

@router.message(lambda message: message.text in LANGUAGES.values())
async def language_selected(message: types.Message):
    user_id = message.from_user.id
    # Находим код языка по значению с флагом
    lang_code = next((code for code, name in LANGUAGES.items() if name == message.text), "en")
    await save_language(user_id, lang_code)

    await message.answer(get_text(lang_code, "language_chosen", "Мову вибрано ✅"))
    await ask_time(message)

@router.message()
async def handle_time_or_text(message: types.Message):
    user_id = message.from_user.id
    user = await get_user(user_id)
    if not user:
        # Новый пользователь, попросить выбрать язык
        await save_user(user_id)
        await ask_language(message)
        return

    lang = user.get("lang") or "en"
    user_time = user.get("time")

    if not user_time:
        text = message.text.strip()
        # Проверяем формат времени ГГ:ХХ
        if re.match(r"^\d{1,2}:\d{2}$", text):
            h, m = map(int, text.split(":"))
            if 0 <= h < 24 and 0 <= m < 60:
                await update_user(user_id, {"time": text})
                await message.answer(get_text(lang, "time_saved", "Час збережено ✅"))
                await message.answer(get_text(lang, 'menu'), reply_markup=main_menu(lang))
            else:
                await message.answer(get_text(lang, "time_format_error", "Невірний формат часу. Введіть у форматі ГГ:ХХ."))
        else:
            await message.answer(get_text(lang, "time_format_error", "Невірний формат часу. Введіть у форматі ГГ:ХХ."))
        return

    # Проверяем лимит перед генерацией контента
    if not await can_use(user_id):
        await message.answer(get_text(lang, "limit_reached", "Ви досягли ліміту на сьогодні. Спробуйте завтра 🙏"))
        return

    await increase(user_id)
    reply = await generate_content_from_text(user_id, message.text)
    await message.answer(reply)
