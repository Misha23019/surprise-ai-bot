from aiogram import types, Router, F
from aiogram.filters import CommandStart
from modules.lang import get_text, ask_language, ask_time
from modules.limits import can_use, increase
from modules.content import generate_content
from modules.database import get_user, save_user
from modules.scheduler import start_scheduler

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
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
    if not await is_allowed(user_id):
        await message.answer("Ви досягли ліміту на сьогодні. Спробуйте завтра 🙏")
        return

    await decrease_limit(user_id)
    await generate_content(message)
