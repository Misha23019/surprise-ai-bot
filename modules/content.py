from modules.telegram import bot
from modules.gpt_api import ask_gpt

async def generate_content(message):
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

    reply = await ask_gpt(prompt)
    await message.answer(reply)

async def generate_scheduled_content(user_id, lang):
    prompt = "Зроби добрий сюрприз на ранок"
    reply = await ask_gpt(prompt, lang)
    await bot.send_message(user_id, reply)
