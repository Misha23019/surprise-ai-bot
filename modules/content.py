from modules.bot import bot
from modules.gpt_api import ask_gpt

# Генерация контента по готовой кнопке / сообщению
async def generate_content_from_message(message):
    text = message.text.lower()
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
        reply = await ask_gpt([{"role": "user", "content": prompt}])
    except Exception:
        reply = "⚠️ Помилка генерації відповіді."
    await message.answer(reply)

# Генерация по пользовательскому вводу (свободное сообщение)
async def generate_content_from_text(user_id: int, user_text: str) -> str:
    messages = [{"role": "user", "content": user_text}]
    try:
        return await ask_gpt(messages)
    except Exception:
        return "⚠️ Виникла помилка при зверненні до GPT."

# Генерация запланированного контента (в 10:00)
async def generate_scheduled_content(user_id, lang):
    prompt = "Зроби добрий сюрприз на ранок"
    try:
        reply = await ask_gpt([{"role": "user", "content": prompt}])
        await bot.send_message(user_id, reply)
    except Exception:
        # Лучше логировать ошибку, чтобы не молчать при падении
        import logging
        logging.error(f"Не вдалося надіслати запланований сюрприз користувачу {user_id}")
