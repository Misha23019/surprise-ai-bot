from aiogram import Router, types
from aiogram.filters import CommandStart
from modules.lang import ask_language, ask_time, get_text, save_language
from modules.database import get_user, update_user
from modules.texts import LANGUAGES
import re

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await ask_language(message)

@router.message()
async def lang_or_time_handler(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    user = await get_user(user_id)
    if not user:
        # Если пользователя еще нет — создаём с дефолтом
        await update_user(user_id, {"lang": None, "time": None})
        await ask_language(message)
        return

    if user.get("lang") is None:
        # Ожидаем выбор языка
        if text in LANGUAGES.values():
            # Определяем код языка по названию
            lang_code = next((code for code, name in LANGUAGES.items() if name == text), None)
            if lang_code:
                await save_language(user_id, lang_code)
                await message.answer(get_text(lang_code, "language_chosen"))
                await ask_time(message)
            else:
                await message.answer("Невідомий вибір мови. Будь ласка, оберіть мову з кнопок.")
        else:
            await message.answer("Будь ласка, оберіть мову за допомогою кнопок нижче.")
        return

    if user.get("time") is None:
        # Ожидаем ввод времени в формате HH:MM
        if re.match(r"^\d{1,2}:\d{2}$", text):
            h, m = map(int, text.split(":"))
            if 0 <= h < 24 and 0 <= m < 60:
                await update_user(user_id, {"time": text})
                lang = user.get("lang")
                await message.answer(get_text(lang, "time_saved"))
                # Показываем главное меню
                # Здесь можно вызвать функцию для показа меню (в зависимости от твоей реализации)
                # Например:
                # await show_main_menu(message, lang)
            else:
                await message.answer("Невірний формат часу. Введіть час у форматі ГГ:ХХ.")
        else:
            await message.answer("Невірний формат часу. Введіть час у форматі ГГ:ХХ.")
        return

    # Если язык и время уже заданы, можно обрабатывать другие команды/сообщения

