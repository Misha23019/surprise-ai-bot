from modules.lang import LANGUAGES, get_text, get_user_lang, set_user_lang, set_user_time
from modules.content import generate_surprise, generate_random
from modules.gpt import generate_gpt_response
from modules.utils import validate_time_format  # допустим, там функция проверки времени

# Глобальный словарь состояний пользователей (в идеале — в отдельном модуле, но пока так)
user_states = {}

def handle_message(user_id, text):
    user_id = str(user_id)
    lang = get_user_lang(user_id) or "en"

    # Инициализируем состояние пользователя, если нет
    if user_id not in user_states:
        user_states[user_id] = {"state": None, "lang": lang}
    else:
        # Обновляем язык в локальном состоянии если он изменился глобально
        if user_states[user_id].get("lang") != lang:
            user_states[user_id]["lang"] = lang

    state = user_states[user_id].get("state")
    texts = get_text(user_states[user_id].get("lang", "en"))

    # Обработка состояния ожидания времени
    if state == "await_time":
        if validate_time_format(text):
            set_user_time(user_id, text)
            user_states[user_id]["state"] = None
            return f"⏰ {texts['change_time']} збережено: {text}. Дякуємо!"
        else:
            return "❌ Невірний формат часу. Введіть у форматі ГГ:ХХ (наприклад, 09:30)."

    # Обработка состояния ожидания ингредиентов для рецепта
    if state == "await_ingredients":
        user_states[user_id]["state"] = None
        prompt = (
            f"Будь ласка, створи детальний рецепт страви, використовуючи ці інгредієнти: {text}"
            if lang == "uk"
            else f"Please create a detailed recipe using these ingredients: {text}"
        )
        return generate_gpt_response(prompt, lang)

    # Обработка команды смены языка через /lang <код>
    if text.startswith("/lang "):
        new_lang = text.split(" ", 1)[1].strip()
        if new_lang in LANGUAGES:
            set_user_lang(user_id, new_lang)
            user_states[user_id] = {"state": None, "lang": new_lang}
            texts = get_text(new_lang)
            return f"✅ {texts['language_changed']}\n\n{texts['ask_time']}"
        else:
            return "❌ Unsupported language code."

    # Обработка запроса изменения времени
    if text == texts["change_time"]:
        user_states[user_id]["state"] = "await_time"
        return texts["ask_time"]

    # Обработка запроса изменения языка
    if text == texts["change_lang"]:
        user_states[user_id]["state"] = None
        return texts["start_choose_lang"]

    text_lower = text.lower()

    # Словарь ключевых слов и соответствующих действий
    commands = {
        "surprise": ("surprise", {
            "uk": "Створи короткий, цікавий сюрприз українською",
            "en": "Create a short, interesting surprise in English"
        }),
        "quote": ("quote", {
            "uk": "Наведи надихаючу цитату українською",
            "en": "Provide an inspiring quote in English"
        }),
        "music": ("music", {
            "uk": "Порадь популярну пісню українською",
            "en": "Recommend a popular song in English"
        }),
        "movie": ("movie", {
            "uk": "Порадь цікавий фільм українською",
            "en": "Recommend an interesting movie in English"
        }),
    }

    # Проверяем команды из словаря
    for key, (content_type, prompts) in commands.items():
        if any(word in text_lower for word in [texts[key].lower(), key, key.capitalize()]):
            prompt = prompts.get(lang, prompts["en"])
            return generate_gpt_response(prompt, lang)

    # Обработка рандома
    if any(word in text_lower for word in [texts["random"].lower(), "рандом", "random"]):
        return generate_random(lang)

    # Обработка рецепта (вход в состояние ожидания ингредиентов)
    if any(word in text_lower for word in [texts["recipe"].lower(), "рецепт", "recipe"]):
        user_states[user_id]["state"] = "await_ingredients"
        return texts["ask_ingredients"]

    # Если ничего не подошло — случайный сюрприз
    return generate_surprise(lang)
