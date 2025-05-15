# Словарь поддерживаемых языков
LANGUAGES = {
    "uk": "Українська", "en": "English", "fr": "Français", "de": "Deutsch", "es": "Español",
    "it": "Italiano", "pl": "Polski", "ru": "Русский", "ro": "Română", "tr": "Türkçe",
    "pt": "Português", "nl": "Nederlands", "sv": "Svenska", "no": "Norsk", "fi": "Suomi",
    "da": "Dansk", "cs": "Čeština", "sk": "Slovenčina", "hu": "Magyar", "bg": "Български",
    "el": "Ελληνικά", "hi": "हिन्दी", "zh": "中文", "ja": "日本語", "ko": "한국어"
}

user_langs = {}

def get_user_lang(chat_id):
    return user_langs.get(chat_id, "uk")

def set_user_lang(chat_id, lang_code):
    user_langs[chat_id] = lang_code

PROMPT_TEMPLATES = {
    "uk": "Напиши щось цікаве або сюрприз: {user_input}",
    "en": "Write something fun or surprising: {user_input}",
    "fr": "Écris quelque chose d'amusant ou de surprenant : {user_input}",
    "de": "Schreibe etwas Lustiges oder Überraschendes: {user_input}",
    "es": "Escribe algo divertido o sorprendente: {user_input}",
    # ... Добавь остальные языки при желании
}

def get_prompt_template(lang_code):
    return PROMPT_TEMPLATES.get(lang_code, PROMPT_TEMPLATES["en"])
