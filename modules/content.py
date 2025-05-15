import random

# Основні словники контенту по мовах
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
    ]
}

RECIPES_BY_LANG = {
    "uk": [
        ("🥗 Овочевий салат", ["огірки", "помідори", "оливкова олія", "сіль"]),
        ("🍲 Курячий суп", ["курка", "морква", "цибуля", "спеції"]),
        ("🍎 Яблучний пиріг", ["яблука", "тісто", "кориця", "цукор"])
    ],
    "en": [
        ("🥗 Vegetable salad", ["cucumbers", "tomatoes", "olive oil", "salt"]),
        ("🍲 Chicken soup", ["chicken", "carrot", "onion", "spices"]),
        ("🍎 Apple pie", ["apples", "dough", "cinnamon", "sugar"])
    ]
}

QUOTES = {
    "uk": [
        "🌟 Цитата дня: «Життя — це те, що трапляється, поки ти плануєш інші справи.»",
        "💡 Цитата дня: «Успіх — це вміння йти від невдачі до невдачі, не втрачаючи ентузіазму.»"
    ],
    "en": [
        "🌟 Quote of the day: \"Life is what happens when you're busy making other plans.\"",
        "💡 Quote of the day: \"Success is going from failure to failure without losing enthusiasm.\""
    ]
}

MUSIC = {
    "uk": ["🎵 Слухайте українську пісню 'Океан Ельзи – Без бою'."],
    "en": ["🎵 Listen to the song 'Imagine' by John Lennon."]
}

MOVIES = {
    "uk": ["🎬 Фільм дня: 'Тіні забутих предків'."],
    "en": ["🎬 Movie of the day: 'Inception'."]
}

RANDOMS = {
    "uk": ["🎲 Випадкова порада: пийте більше води!"],
    "en": ["🎲 Random tip: drink more water!"]
}

TIME_REQUEST_TEXT = {
    "uk": "🕒 Будь ласка, введіть ваше поточне час у форматі ГГ:ХХ.",
    "en": "🕒 Please enter your current time in HH:MM format."
}

LIMIT_REACHED_TEXT = {
    "uk": "⚠️ Ви досягли ліміту в 5 запитів на день. Спробуйте завтра!",
    "en": "⚠️ You have reached the limit of 5 requests per day. Please try again tomorrow!"
}

MAIN_MENU_BUTTONS = {
    "uk": ["🎲 Сюрприз", "🎬 Фільм", "🎵 Музика", "📝 Цитата", "🎲 Рандом", "🍽 Рецепт"],
    "en": ["🎲 Surprise", "🎬 Movie", "🎵 Music", "📝 Quote", "🎲 Random", "🍽 Recipe"]
}

SETTINGS_MENU = {
    "uk": "⚙️ Налаштування",
    "en": "⚙️ Settings"
}

# --- Генератори контенту --- #

def generate_surprise(lang):
    items = SURPRISES.get(lang, SURPRISES["en"])
    return random.choice(items)

def generate_quote(lang):
    items = QUOTES.get(lang, QUOTES["en"])
    return random.choice(items)

def generate_music(lang):
    items = MUSIC.get(lang, MUSIC["en"])
    return random.choice(items)

def generate_movie(lang):
    items = MOVIES.get(lang, MOVIES["en"])
    return random.choice(items)

def generate_random(lang):
    items = RANDOMS.get(lang, RANDOMS["en"])
    return random.choice(items)

def generate_recipe(ingredients_text, lang):
    recipes = RECIPES_BY_LANG.get(lang, RECIPES_BY_LANG["en"])
    ingredients_input = [i.strip().lower() for i in ingredients_text.split(",")]

    matches = []
    for title, ingredients in recipes:
        if any(ing in [i.lower() for i in ingredients] for ing in ingredients_input):
            matches.append(title + ": " + ", ".join(ingredients))

    if matches:
        return f"🍽 Рецепт за вашими інгредієнтами:\n" + random.choice(matches)
    else:
        return "😔 Нажаль, я не знайшов рецепту з такими інгредієнтами."

