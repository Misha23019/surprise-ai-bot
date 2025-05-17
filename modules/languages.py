# modules/languages.py

LANGUAGES = {
    "uk": "🇺🇦 Українська",
    "en": "🇬🇧 English",
    "pl": "🇵🇱 Polski",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "it": "🇮🇹 Italiano",
    "pt": "🇵🇹 Português",
    "ro": "🇷🇴 Română",
    "nl": "🇳🇱 Nederlands",
    "cs": "🇨🇿 Čeština",
    "sk": "🇸🇰 Slovenčina",
    "sv": "🇸🇪 Svenska",
    "no": "🇳🇴 Norsk",
    "fi": "🇫🇮 Suomi",
    "hu": "🇭🇺 Magyar",
    "tr": "🇹🇷 Türkçe",
    "el": "🇬🇷 Ελληνικά",
    "bg": "🇧🇬 Български",
    "sr": "🇷🇸 Српски",
    "hr": "🇭🇷 Hrvatski",
    "lt": "🇱🇹 Lietuvių",
    "lv": "🇱🇻 Latviešu",
    "et": "🇪🇪 Eesti",
    "ru": "🇷🇺 Русский"
}

def get_flag(lang_code: str) -> str:
    return LANGUAGES.get(lang_code, "🏳")
