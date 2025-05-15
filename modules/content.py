# modules/content.py

# Примерные тексты приветствий и объяснений
GREETINGS = {
    "uk": "👋 Вітаю! Оберіть мову командою типу /lang uk",
    "en": "👋 Hello! Please choose your language with a command like /lang en",
    "ru": "👋 Привет! Выберите язык командой, например /lang ru",
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

# Сюрпризы по языкам (можно расширить)
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
    # Добавь по другим языкам, если нужно
}

# Рецепты (пример с несколькими, можно расширить и сделать с фильтрами по ингредиентам)
RECIPES = {
    "default": [
        "🥗 Овочевий салат: огірки, помідори, оливкова олія, сіль.",
        "🍲 Курячий суп: курка, морква, цибуля, спеції.",
        "🍎 Яблучний пиріг: яблука, тісто, кориця, цукор."
    ]
}

# Объяснение запроса времени
TIME_REQUEST_TEXT = {
    "uk": (
        "Будь ласка, введіть ваше поточне час у форматі ГГ:ХХ.\n"
        "Це потрібно, щоб щоденний автоматичний контент генерувався для вас о 10:00 за вашим часом."
    ),
    "en": (
        "Please enter your current time in HH:MM format.\n"
        "This is needed so that daily auto-generated content can be sent to you at 10:00 your local time."
    ),
    # Добавь для других языков, если нужно
}

# Текст ошибки лимита
LIMIT_REACHED_TEXT = {
    "uk": "⚠️ Ви досягли ліміту в 5 запитів на день. Спробуйте завтра!",
    "en": "⚠️ You have reached the limit of 5 requests per day. Please try again tomorrow!",
}

# Верхнее меню (кнопки)
MAIN_MENU_BUTTONS = {
    "uk": ["🎲 Сюрприз", "🎬 Фільм", "🎵 Музика", "📝 Цитата", "🎲 Рандом", "🍽 Рецепт"],
    "en": ["🎲 Surprise", "🎬 Movie", "🎵 Music", "📝 Quote", "🎲 Random", "🍽 Recipe"],
}

# Кнопки настроек (смена языка и времени)
SETTINGS_MENU = {
    "uk": "⚙️ Налаштування",
    "en": "⚙️ Settings",
}

# Добавляй сюда другие тексты, шаблоны и данные, которые нужны для проекта

