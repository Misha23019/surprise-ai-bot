from modules.content import (
    generate_surprise,
    generate_recipe,
    generate_quote,
    generate_music,
    generate_movie,
    generate_random,
)
from modules.lang import get_text, set_user_lang, get_user_lang

# Для примера: словарь для хранения состояний пользователей в памяти
# В проде лучше использовать БД или файлы
user_states = {}  # user_id -> {"state": "await_time" / "await_ingredients" / None, "lang": "uk"}

user_times = {}   # user_id -> строка с временем "HH:MM"

def handle_message(user_id, text):
    # Получаем язык пользователя из сохранённого состояния или по умолчанию
    lang = user_states.get(user_id, {}).get("lang", get_user_lang(user_id))

    # Получаем тексты для языка
    texts = get_text(lang)

    # Проверяем, есть ли у пользователя активное состояние (например, он вводит время или ингредиенты)
    state = user_states.get(user_id, {}).get("state")

    if state == "await_time":
        # Ожидаем время в формате HH:MM
        if validate_time_format(text):
            user_times[user_id] = text
            user_states[user_id]["state"] = None  # Сброс состояния
            return f"⏰ Час збережено: {text}. Дякую!"
        else:
            return "❌ Невірний формат часу. Введіть у форматі ГГ:ХХ (наприклад, 09:30)."

    elif state == "await_ingredients":
        # Ожидаем список ингредиентов
        user_states[user_id]["state"] = None
        # Передаем ингредиенты в генератор рецептов
        return generate_recipe(text, lang)

    # Если пришла команда смены языка (например /lang uk)
    if text.startswith("/lang "):
        new_lang = text.split(" ", 1)[1].strip()
        if new_lang in get_text(new_lang):  # Проверяем, поддерживаем ли язык
            set_user_lang(user_id, new_lang)
            user_states[user_id] = {"state": None, "lang": new_lang}
            return texts["language_changed"]
        else:
            return "❌ Unsupported language code."

    # Если команда смены времени
    if text == texts["change_time"]:
        user_states[user_id]["state"] = "await_time"
        return texts["ask_time"]

    # Если команда смены языка через кнопку
    if text == texts["change_lang"]:
        user_states[user_id]["state"] = None
        return texts["start_choose_lang"]

    # Обработка основных команд по ключевым словам
    text_lower = text.lower()

    if texts["surprise"].lower() in text_lower or "сюрприз" in text_lower or "surprise" in text_lower:
        return generate_surprise(lang)

    elif texts["quote"].lower() in text_lower or "цитата" in text_lower or "quote" in text_lower:
        return generate_quote(lang)

    elif texts["music"].lower() in text_lower or "музика" in text_lower or "музыка" in text_lower or "music" in text_lower:
        return generate_music(lang)

    elif texts["movie"].lower() in text_lower or "фильм" in text_lower or "movie" in text_lower:
        return generate_movie(lang)

    elif texts["random"].lower() in text_lower or "рандом" in text_lower or "random" in text_lower:
        return generate_random(lang)

    elif texts["recipe"].lower() in text_lower or "рецепт" in text_lower or "recipe" in text_lower:
        # Запускаем режим ожидания ингредиентов
        user_states[user_id]["state"] = "await_ingredients"
        return texts["ask_ingredients"]

    else:
        # fallback — случайный сюрприз
        return generate_surprise(lang)

def validate_time_format(time_str):
    # Простая валидация формата HH:MM
    import re
    return bool(re.match(r"^([01]\d|2[0-3]):[0-5]\d$", time_str))
