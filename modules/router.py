from modules.content import (
    generate_surprise,
    generate_recipe,
    generate_quote,
    generate_music,
    generate_movie,
    generate_random,
)
from modules.lang import get_text, set_user_lang, get_user_lang, set_user_time

# Тимчасове сховище станів користувачів у пам'яті
user_states = {}  # user_id -> {"state": ..., "lang": ...}

def handle_message(user_id, text):
    user_id = str(user_id)

    # Отримуємо мову користувача (з памʼяті або з файлу)
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
        return generate_recipe(text, lang)

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


def validate_time_format(time_str):
    import re
    return bool(re.match(r"^([01]\d|2[0-3]):[0-5]\d$", time_str))
