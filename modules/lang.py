# modules/lang.py

LANGUAGES = {
    "en": "English",
    "uk": "Українська",
    "ru": "Русский",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "pl": "Polski",
    "nl": "Nederlands",
    "sv": "Svenska",
    "fi": "Suomi",
    "no": "Norsk",
    "da": "Dansk",
    "cs": "Čeština",
    "hu": "Magyar",
    "ro": "Română",
    "bg": "Български",
    "el": "Ελληνικά",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "中文",
    "ar": "العربية",
    "he": "עברית",
    "tr": "Türkçe",
}

TEXTS = {
    "welcome": {
        "en": "Welcome! Please choose your language.",
        "uk": "Ласкаво просимо! Виберіть вашу мову.",
        "ru": "Добро пожаловать! Пожалуйста, выберите язык.",
        "es": "¡Bienvenido! Por favor, elige tu idioma.",
        "fr": "Bienvenue ! Veuillez choisir votre langue.",
        "de": "Willkommen! Bitte wählen Sie Ihre Sprache.",
        # ... остальные переводы
    },
    "ask_time": {
        "en": "What time is it now for you? (HH:MM)",
        "uk": "Котра зараз година? (ГГ:ХХ)",
        "ru": "Который сейчас час? (ЧЧ:ММ)",
        # ... остальные переводы
    },
    "limit_exceeded": {
        "en": "You've reached today's limit of surprises 😉",
        "uk": "Ви досягли ліміту сюрпризів на сьогодні 😉",
        "ru": "Вы достигли лимита сюрпризов на сегодня 😉",
        # ... остальные переводы
    },
    "auto_surprise_text": {
        "en": "🎁 Your daily surprise!",
        "uk": "🎁 Ваш щоденний сюрприз!",
        "ru": "🎁 Ваш ежедневный сюрприз!",
        # ... остальные переводы
    },
    # Добавляйте остальные тексты...
}

def get_text(key: str, lang: str = "en") -> str:
    """Возвращает текст по ключу и языку.
    Если нет перевода, возвращает на английском или ключ."""
    if key not in TEXTS:
        return key
    return TEXTS[key].get(lang) or TEXTS[key].get("en") or key

def get_languages():
    """Возвращает словарь языков."""
    return LANGUAGES
