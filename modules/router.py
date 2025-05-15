import os
import requests
from modules.content import (
    generate_surprise,
    generate_quote,
    generate_music,
    generate_movie,
    generate_random,
)
from modules.lang import get_text, set_user_lang, get_user_lang, set_user_time

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Тимчасове сховище станів користувачів у пам'яті
user_states = {}  # user_id -> {"state": ..., "lang": ...}

def generate_gpt_response(prompt, lang="en"):
    if not OPENROUTER_API_KEY:
        return "⚠️ Відсутній ключ API для генерації AI-відповідей."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    system_message = "You are a helpful assistant."
    if lang == "uk":
        system_message = "Ви - корисний помічник, який відповідає українською."

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=data,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Помилка при зверненні до AI: {e}"

def validate_time_format(time_str):
    import re
    return bool(re.match(r"^([01]\d|2[0-3]):[0-5]\d$", time_str))

def handle_message(user_id, text):
    user_id = str(user_id)

    # Отримуємо мову користувача
    lang = user_states.get(user_id, {}).get("lang", get_user_lang(user_id))
    texts = get_text(lang)

    # Поточний стан користувача
    state = user_states.get(user_id, {}).get("state")

    # --- Очікуємо введення часу ---
    if state == "await_time":
        if validate_time_format(text):
            set_user_time(user_id, text)
            user_states[user_id]["state"] = None
            return f"⏰ {texts['change_time']} збережено: {text}. Дякуємо!"
        else:
            return "❌ Невірний формат часу. Введіть у форматі ГГ:ХХ (наприклад, 09:30)."

    # --- Очікуємо введення інгредієнтів ---
    if state == "await_ingredients":
        user_states[user_id]["state"] = None
        # Генеруємо рецепт через GPT
        prompt = f"Зроби рецепт за інгредієнтами: {text}"
        if lang == "uk":
            prompt = f"Будь ласка, створи детальний рецепт страви, використовуючи ці інгредієнти: {text}"
        return generate_gpt_response(prompt, lang)

    # --- Зміна мови через команду /lang ---
    if text.startswith("/lang "):
        new_lang = text.split(" ", 1)[1].strip()
        if new_lang in get_text(new_lang):
            set_user_lang(user_id, new_lang)
            user_states[user_id] = {"state": None, "lang": new_lang}
            texts = get_text(new_lang)
            return f"✅ {texts['language_changed']}\n\n{texts['ask_time']}"
        else:
            return "❌ Unsupported language code."

    # --- Кнопка «Змінити час» ---
    if text == texts["change_time"]:
        user_states[user_id] = {"state": "await_time", "lang": lang}
        return texts["ask_time"]

    # --- Кнопка «Змінити мову» ---
    if text == texts["change_lang"]:
        user_states[user_id]["state"] = None
        return texts["start_choose_lang"]

    # --- Основні команди та ключові слова ---
    text_lower = text.lower()

    if any(word in text_lower for word in [texts["surprise"].lower(), "сюрприз", "surprise"]):
        return generate_surprise(lang)

    if any(word in text_lower for word in [texts["quote"].lower(), "цитата", "quote"]):
        return generate_quote(lang)

    if any(word in text_lower for word in [texts["music"].lower(), "музика", "музыка", "music"]):
        return generate_music(lang)

    if any(word in text_lower for word in [texts["movie"].lower(), "фільм", "фильм", "movie"]):
        return generate_movie(lang)

    if any(word in text_lower for word in [texts["random"].lower(), "рандом", "random"]):
        return generate_random(lang)

    if any(word in text_lower for word in [texts["recipe"].lower(), "рецепт", "recipe"]):
        user_states[user_id] = {"state": "await_ingredients", "lang": lang}
        return texts["ask_ingredients"]

    # --- За замовчуванням — генеруємо сюрприз ---
    return generate_surprise(lang)
