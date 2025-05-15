import json
import os

LANGUAGES = {
    "uk": "Українська",
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español",
    "it": "Italiano",
    "pl": "Polski",
    "ru": "Русский",
    "ro": "Română",
    "tr": "Türkçe",
    "pt": "Português",
    "nl": "Nederlands",
    "sv": "Svenska",
    "no": "Norsk",
    "fi": "Suomi",
    "da": "Dansk",
    "cs": "Čeština",
    "sk": "Slovenčina",
    "hu": "Magyar",
    "bg": "Български",
    "el": "Ελληνικά",
    "hi": "हिन्दी",
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어",
}

LANG_FILE = "data/langs.json"

def load_lang_data():
    if os.path.exists(LANG_FILE):
        with open(LANG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_lang_data(data):
    os.makedirs(os.path.dirname(LANG_FILE), exist_ok=True)
    with open(LANG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def get_user_lang(user_id):
    data = load_lang_data()
    return data.get(str(user_id), "uk")

def set_user_lang(user_id, lang_code):
    data = load_lang_data()
    data[str(user_id)] = lang_code
    save_lang_data(data)

# Универсальный словарь текста по ключам (можно расширять)
TEXTS = {
    "uk": {
        "start_choose_lang": "👋 Вітаю! Оберіть мову командою типу /lang uk\n\n🌐 Доступні мови:\n" + "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()]),
        "language_changed": "✅ Мова змінена на Українська",
        "ask_time": "⏰ Вкажіть ваш поточний час у форматі ГГ:ХХ\n(Це потрібно, щоб щодня о 10:00 надсилати персональний сюрприз!)",
        "surprise": "🎲 Сюрприз",
        "movie": "🎬 Фільм",
        "music": "🎵 Музика",
        "quote": "💬 Цитата",
        "random": "🔀 Рандом",
        "recipe": "🍽️ Рецепт",
        "change_lang": "🌐 Змінити мову",
        "change_time": "⏰ Змінити час",
        "ask_ingredients": "🥦 Введіть список продуктів через кому (наприклад: картопля, морква, цибуля):"
    },
    "en": {
        "start_choose_lang": "👋 Welcome! Choose your language using a command like /lang en\n\n🌐 Available languages:\n" + "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()]),
        "language_changed": "✅ Language changed to English",
        "ask_time": "⏰ Please enter your current time (HH:MM format).\n(This is used to send you daily AI content at 10:00)",
        "surprise": "🎲 Surprise",
        "movie": "🎬 Movie",
        "music": "🎵 Music",
        "quote": "💬 Quote",
        "random": "🔀 Random",
        "recipe": "🍽️ Recipe",
        "change_lang": "🌐 Change Language",
        "change_time": "⏰ Change Time",
        "ask_ingredients": "🥦 Enter ingredients separated by commas (e.g., potatoes, carrots, onion):"
    },
    # Добавь остальные языки по аналогии
}

def get_text(lang_code):
    return TEXTS.get(lang_code, TEXTS["uk"])
