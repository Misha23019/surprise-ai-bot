# Словарь поддерживаемых языков
LANGUAGES = {
    "uk": "Українська", "en": "English", "fr": "Français", "de": "Deutsch", "es": "Español",
    "it": "Italiano", "pl": "Polski", "ru": "Русский", "ro": "Română", "tr": "Türkçe",
    "pt": "Português", "nl": "Nederlands", "sv": "Svenska", "no": "Norsk", "fi": "Suomi",
    "da": "Dansk", "cs": "Čeština", "sk": "Slovenčina", "hu": "Magyar", "bg": "Български",
    "el": "Ελληνικά", "hi": "हिन्दी", "zh": "中文", "ja": "日本語", "ko": "한국어"
}

user_langs = {}
user_times = {}

def get_user_lang(chat_id):
    return user_langs.get(chat_id, "uk")

def set_user_lang(chat_id, lang_code):
    user_langs[chat_id] = lang_code

def get_user_time(chat_id):
    return user_times.get(chat_id)

def set_user_time(chat_id, time_str):
    user_times[chat_id] = time_str

PROMPT_TEMPLATES = {
    "uk": "Напиши щось цікаве або сюрприз: {user_input}",
    "en": "Write something fun or surprising: {user_input}",
    "fr": "Écris quelque chose d'amusant ou de surprenant : {user_input}",
    "de": "Schreibe etwas Lustiges oder Überraschendes: {user_input}",
    "es": "Escribe algo divertido o sorprendente: {user_input}",
    # Добавь остальные языки по желанию
}

def get_prompt_template(lang_code):
    return PROMPT_TEMPLATES.get(lang_code, PROMPT_TEMPLATES["en"])

# Новые строки для мультиязычного интерфейса
ASK_TIME = {
    "uk": "⏰ Вкажіть поточний час у форматі ГГ:ХХ (наприклад, 09:30), щоб ми могли надсилати сюрпризи щодня о 10:00!",
    "en": "⏰ Please enter your current time in HH:MM format (e.g., 09:30) so we can send daily surprises at 10:00!",
    # ... переводы для остальных языков
}

TIME_SAVED = {
    "uk": "✅ Час збережено! Щоденні сюрпризи приходитимуть о 10:00 за вашим часом.",
    "en": "✅ Time saved! Daily surprises will arrive at 10:00 your time.",
    # ... переводы для остальных языков
}

ASK_INGREDIENTS = {
    "uk": "🥕 Введіть список інгредієнтів через кому, і я підберу рецепти!",
    "en": "🥕 Enter a list of ingredients separated by commas, and I'll suggest recipes!",
    # ... переводы для остальных языков
}

def get_localized_text(chat_id, dictionary):
    lang = get_user_lang(chat_id)
    return dictionary.get(lang, dictionary["en"])
