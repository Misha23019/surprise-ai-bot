# modules/telegram.py
from aiogram import Router, F
from aiogram.types import Message
from modules.limits import can_use, increase
from modules.gpt_api import ask_qwen


router = Router()

@router.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    if not can_use(user_id):
        await message.answer("Извините, лимит на сегодня исчерпан.")
        return

    increase(user_id)

    messages = [{"role": "user", "content": message.text}]
    try:
        response = ask_qwen(messages)
        await message.answer(response)
    except Exception:
        await message.answer("Произошла ошибка при обращении к GPT")

def setup_handlers(dp):
   dp.include_router(main_router)  # start, settings, content
   dp.include_router(router)  # GPT-обработчик
