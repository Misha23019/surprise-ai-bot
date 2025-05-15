from modules.ai import ask_openrouter
from modules.lang import (
    get_user_lang,
    set_user_lang,
    LANGUAGES,
    get_localized_text,
    set_user_time,
    get_user_time,
)
from modules.telegram import build_keyboard
import re

# Состояния пользователя (например, ожидание ингредиентов)
user_states = {}

def generate_response(user_input, chat_id):
    lang = get_user_lang(chat_id)
    time = get_user_time(chat_id)

    # Проверка: не задано ли ещё время
    if not time:
        # Проверка формата времени
        if re.match(r"^\d{1,2}:\d{2}$", user_input.strip()):
            set_user_time(chat_id, user_input.strip())
            return get_localized_text(chat_id, {
                "uk": f"✅ Час збережено: {user_input.strip()}\n\nТепер обери кнопку внизу ⬇️",
                "en": f"✅ Time saved: {user_input.strip()}\n\nNow pick a button below ⬇️",
            })
        else:
            return get_localized_text(chat_id, {
                "uk": "🕒 Введіть ваш поточний час у форматі ГГ:ХХ (наприклад, 09:30), щоб отримувати сюрпризи о 10:00.",
                "en": "🕒 Please enter your current time in HH:MM format (e.g., 09:30) to receive surprises at 10:00.",
            })

    # Обработка кнопок
    if user_input in ["🎲 Сюрприз", "🎬 Фільм", "🎵 Музика", "💬 Цитата", "❓ Рандом"]:
        prompt = {
            "🎲 Сюрприз": "Згенеруй креативний сюрприз на день",
            "🎬 Фільм": "Порекомендуй хороший фільм",
            "🎵 Музика": "Запропонуй цікаву пісню",
            "💬 Цитата": "Поділись мудрою цитатою",
            "❓ Рандом": "Зроби щось абсолютно випадкове",
        }[user_input]
        return ask_openrouter(prompt, lang)

    # Обработка рецептов
    if user_input == "🍲 Рецепт":
        user_states[chat_id] = "waiting_ingredients"
        return get_localized_text(chat_id, {
            "uk": "📝 Введіть список продуктів через кому (наприклад: яйця, сир, хліб)",
            "en": "📝 Enter a list of ingredients separated by commas (e.g., eggs, cheese, bread)",
        })

    if user_states.get(chat_id) == "waiting_ingredients":
        user_states.pop(chat_id, None)
        prompt = f"Запропонуй 2-3 рецепти зі списку інгредієнтів: {user_input}"
        return ask_openrouter(prompt, lang)

    # Стандартна відповідь через AI
    return ask_openrouter(user_input, lang)
