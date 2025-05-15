from modules.lang import get_text

def generate_surprise(lang):
    # Здесь можно добавить вызов GPT, сейчас заглушка
    return get_text("surprise_example", lang) or "🎁 Ось ваш сюрприз!"

def generate_movie(lang):
    return get_text("movie_example", lang) or "🎬 Спробуйте подивитись фільм «Назва»."

def generate_music(lang):
    return get_text("music_example", lang) or "🎵 Послухайте музику «Назва пісні»."

def generate_quote(lang):
    return get_text("quote_example", lang) or "💬 Цитата на сьогодні: «Все починається з мрії.»"

def generate_random(lang):
    return get_text("random_example", lang) or "🎲 Ось випадковий сюрприз для вас!"

def generate_recipe(lang, ingredients):
    # Просто для примера объединяем ингредиенты
    ingr_text = ", ".join(ingredients)
    return get_text("recipe_example", lang).format(ingredients=ingr_text) or f"🍳 Ось рецепт з інгредієнтами: {ingr_text}."
