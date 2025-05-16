from aiogram import Router, types, F
from aiogram.types import Message
from modules.bot import bot, dp
from modules.limits import can_use, increase

router = Router()

@router.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id

    if not can_use(user_id):
        await message.answer("Извините, лимит на сегодня исчерпан.")
        return

    increase(user_id)
    await message.answer("Ваш запрос принят!")  # Здесь будет вызов GPT
