# modules/content.py

import random

# Словарь языков (если нужно, импортируй из lang.py)
# LANGUAGES = {...}  # предполагается, что у тебя есть этот словарь

GREETINGS = {
    "uk": "👋 Вітаю! Оберіть мову командою типу /lang uk",
    "en": "👋 Hello! Please choose your language with a command like /lang en",
    "ru": "👋 Привет! Выберите язык командой, например /lang ru",
    # Добавь остальные языки...
}

LANGUAGE_LIST_TEXT = (
    "🌐 Доступні мови:\n"
    "uk - Українська\n"
    "en - English\n"
    "fr - Français\n"
    "de - Deutsch\n"
    "es - Español\n"
    "it - Italiano\n"
    "pl - Polski\n"
    "ru - Русский\n"
    "ro - Română\n"
    "tr - Türkçe\n"
    "pt - Português\n"
    "nl - Nederlands\n"
    "sv - Svenska\n"
    "no - Norsk\n"
    "fi - Suomi\n"
    "da - Dansk\n"
    "cs - Čeština\n"
    "sk - Slovenčina\n"
    "hu - Magyar\n"
    "bg - Български\n"
    "el - Ελληνικά\n"
    "hi - हिन्दी\n"
    "zh - 中文\n"
    "ja - 日本語\n"
    "ko - 한국어\n"
)

SURPRISES = {
    "uk": [
        "🎉 Сюрприз: сьогодні чудовий день для нових ідей!",
        "🎲 Сюрприз: час зробити щось несподіване!",
        "🌟 Сюрприз: посміхнись, і світ усміхнеться у відповідь!"
    ],
    "en": [
        "🎉 Surprise: today is a great day for new ideas!",
        "🎲 Surprise: time to do something unexpected!",
        "🌟 Surprise: smile and the world will smile back!"
    ],
    # Добавь по другим языкам...
}

RECIPES = {
    "uk": [
        "🥗 Овочевий салат: огірки, помідори, оливкова олія, сіль.",
        "🍲 Курячий суп: курка, морква, цибуля, спеції.",
        "🍎 Яблучний пиріг: яблука, тісто, кориця, цукор."
    ],
    "en": [
        "🥗 Vegetable salad: cucumbers, tomatoes, olive oil, salt.",
        "🍲 Chicken soup: chicken, carrot, onion, spices.",
        "🍎 Apple pie: apples, dough, cinnamon, sugar."
    ],
    # Добавь другие языки
}

QUOTES = {
    "uk": [
        "🌟 Цитата дня: «Життя — це те, що трапляється, поки ти плануєш інші справи.»",
        "💡 Цитата дня: «Успіх — це вміння йти від невдачі до невдачі, не втрачаючи ентузіазму.»"
    ],
    "en": [
        "🌟 Quote of the day: \"Life is what happens when you're busy making other plans.\"",
        "💡 Quote of the day: \"Success is going from failure to failure without losing enthusiasm.\""
    ],
    # Добавь другие языки
}

MUSIC = {
    "uk": [
        "🎵 Слухайте українську пісню 'Океан Ельзи – Без бою'.",
    ],
    "en": [
        "🎵 Listen to the song 'Imagine' by John Lennon.",
    ],
}

MOVIES = {
    "uk": [
        "🎬 Фільм дня: 'Тіні забутих предків'.",
    ],
    "en": [
        "🎬 Movie of the day: 'Inception'.",
    ],
}

RANDOMS = {
    "uk": [
        "🎲 Випадкова порада: пийте більше води!",
    ],
    "en": [
        "🎲 Random tip: drink more water!",
    ],
}

TIME_REQUEST_TEXT = {
    "uk": (
        "Будь ласка, введіть ваше поточне час у форматі ГГ:ХХ.\n"
        "Це потрібно, щоб щоденний автоматичний контент генерувався для вас о 10:00 за вашим часом."
    ),
    "en": (
        "Please enter your current time in HH:MM format.\n"
        "This is needed so that daily auto-generated content can be sent to you at 10:00 your local time."
    ),
    # Добавь другие языки
}

LIMIT_REACHED_TEXT = {
    "uk": "⚠️ Ви досягли ліміту в 5 запитів на день. Спробуйте завтра!",
    "en": "⚠️ You have reached the limit of 5 requests per day. Please try again tomorrow!",
}

MAIN_MENU_BUTTONS = {
    "uk": ["🎲 Сюрприз", "🎬 Фільм", "🎵 Музика", "📝 Цитата", "🎲 Рандом", "🍽 Рецепт"],
    "en": ["🎲 Surprise", "🎬 Movie", "🎵 Music", "📝 Quote", "🎲 Random", "🍽 Recipe"],
}

SETTINGS_MENU = {
    "uk": "⚙️ Налаштування",
    "en": "⚙️ Settings",
}


# Функции генерации контента по языку
def generate_surprise(lang):
    items = SURPRISES.get(lang) or SURPRISES.get("en")
    return random.choice(items)


def generate_recipe(lang):
    items = RECIPES.get(lang) or RECIPES.get("en") or []
    return random.choice(items) if items else "No recipes available."


def generate_quote(lang):
    items = QUOTES.get(lang) or QUOTES.get("en") or []
    return random.choice(items) if items else "No quotes available."


def generate_music(lang):
    items = MUSIC.get(lang) or MUSIC.get("en") or []
    return random.choice(items) if items else "No music suggestions."


def generate_movie(lang):
    items = MOVIES.get(lang) or MOVIES.get("en") or []
    return random.choice(items) if items else "No movies suggestions."


def generate_random(lang):
    items = RANDOMS.get(lang) or RANDOMS.get("en") or []
    return random.choice(items) if items else "No random tips."


# Можно добавить и другие функции по необходимости

