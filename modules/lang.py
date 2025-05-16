LANGUAGES = {
    "en": "English",
    "uk": "Українська",
    "es": "Español",
    "de": "Deutsch",
    "fr": "Français",
    "it": "Italiano",
    "pl": "Polski",
    "pt": "Português",
    "ru": "Русский",
    "tr": "Türkçe",
    "ar": "العربية",
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어",
    "hi": "हिन्दी"
}

DEFAULT_LANG = "en"

TRANSLATIONS = {
    "menu": {
        "en": ["🎁 Surprise", "🎬 Movie", "🎵 Music", "💬 Quote", "🎲 Random", "🍳 Recipe", "⚙ Settings"],
        "uk": ["🎁 Сюрприз", "🎬 Фільм", "🎵 Музика", "💬 Цитата", "🎲 Рандом", "🍳 Рецепт", "⚙ Налаштування"],
        # ... остальные переводы
    },
    "choose_lang": {
        "en": "🌍 Choose your language:",
        "uk": "🌍 Оберіть мову:",
        # ...
    },
    "set_time": {
        "en": "🕒 Please send your local time (e.g., 08:30 or 20:15)",
        "uk": "🕒 Вкажіть свій локальний час (наприклад, 08:30 або 20:15)",
        # ...
    },
    "thanks": {
        "en": "✅ Saved! Use the menu below 👇",
        "uk": "✅ Збережено! Використовуйте меню нижче 👇",
        # ...
    },
    "limit_reached": {
        "en": "🚫 Daily limit reached. Wait until tomorrow!",
        "uk": "🚫 Досягнуто ліміт. Повертайтеся завтра!",
        # ...
    },
}

def get_text(user_lang: str, key: str):
    return TRANSLATIONS.get(key, {}).get(user_lang, TRANSLATIONS.get(key, {}).get(DEFAULT_LANG, "…"))

def get_menu(user_lang: str):
    return TRANSLATIONS["menu"].get(user_lang, TRANSLATIONS["menu"][DEFAULT_LANG])
