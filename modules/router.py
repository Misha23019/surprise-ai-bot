from aiogram import types, Router, F
from aiogram.filters import CommandStart
from modules.lang import get_text, ask_language, ask_time, LANGUAGES
from modules.limits import can_use, increase
from modules.content import generate_content_from_message, generate_content_from_text
from modules.database import get_user, save_user
from modules.scheduler import start_scheduler

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привіт! Я працюю.")
    user_id = message.from_user.id
    user = await get_user(user_id)
    if not user:
        await save_user(user_id)
        await ask_language(message)
    else:
        await message.answer(get_text(user['lang'], 'menu'))

@router.message(F.text.lower().in_({"налаштування", "⚙ налаштування", "settings", "⚙ settings"}))
async def settings_handler(message: types.Message):
    await ask_language(message)

@router.message(F.text.lower().in_({
    "привіт", "hello", "🎁 сюрприз", "🎬 фільм", "🎵 музика", "💬 цитата", "🎲 рандом", "🍳 рецепт"
}))
async def content_request(message: types.Message):
    user_id = message.from_user.id
    if not await can_use(user_id):
        await message.answer("Ви досягли ліміту на сьогодні. Спробуйте завтра 🙏")
        return

    await increase(user_id)
    await generate_content_from_message(message)

@router.message(lambda message: message.text in LANGUAGES.values())
async def language_selected(message: types.Message):
    user_id = message.from_user.id

    # Найти код языка по его названию
    lang_code = next((code for code, name in LANGUAGES.items() if name == message.text), "en")
    await save_language(user_id, lang_code)

    await ask_time(message)
    
@router.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    if not await can_use(user_id):
        await message.answer("Ви досягли ліміту на сьогодні. Спробуйте завтра 🙏")
        return

    await increase(user_id)
    reply = await generate_content_from_text(user_id, message.text)
    await message.answer(reply)

