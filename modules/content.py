from modules.bot import bot
from modules.gpt_api import ask_gpt

# Генерация контента по кнопке / сообщению
async def generate_content_from_message(message):
    text = message.text.lower()
    user_id = str(message.from_user.id)
    prompt = ""

    if "фільм" in text or "movie" in text:
        prompt = "Порекомендуй хороший фільм на вечір"
    elif "музика" in text or "music" in text:
        prompt = "Порекомендуй надихаючу музику"
    elif "цитата" in text or "quote" in text:
        prompt = "Надихни мене цитатою"
    elif "рецепт" in text or "recipe" in text:
        prompt = "Запропонуй легкий і смачний рецепт"
    elif "рандом" in text or "random" in text:
        prompt = "Здивуй мене чимось випадковим"
    else:
        prompt = "Зроби мені сюрприз"

    try:
        reply = await ask_gpt(user_id, [{"role": "user", "content": prompt}])
    except Exception:
        reply = "⚠️ Помилка генерації відповіді."
    await message.answer(reply)

# Генерация по свободному тексту
async def generate_content_from_text(user_id: int, user_text: str) -> str:
    try:
        return await ask_gpt(str(user_id), [{"role": "user", "content": user_text}])
    except Exception:
        return "⚠️ Виникла помилка при зверненні до GPT."

# Генерация по расписанию (автосюрприз)
async def generate_scheduled_content(user_id, lang):
    prompt = "Зроби добрий сюрприз на ранок"
    try:
        reply = await ask_gpt(str(user_id), [{"role": "user", "content": prompt}])
        await bot.send_message(user_id, reply)
    except Exception as e:
        import logging
        logging.error(f"❌ Плановий сюрприз не надіслано для {user_id}: {e}")
