import random

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

def generate_surprise(lang):
    return random.choice(SURPRISES.get(lang, SURPRISES["en"]))

def generate_quote(lang):
    return random.choice(QUOTES.get(lang, QUOTES["en"]))

def generate_music(lang):
    return random.choice(MUSIC.get(lang, MUSIC["en"]))

def generate_movie(lang):
    return random.choice(MOVIES.get(lang, MOVIES["en"]))

def generate_random(lang):
    return random.choice(RANDOMS.get(lang, RANDOMS["en"]))
