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
