from modules.content import generate_surprise, generate_recipe, generate_quote, generate_music, generate_movie, generate_random
from modules.lang import translate


def generate_response(text, lang):
    text_lower = text.lower()

    if "сюрприз" in text_lower or "surprise" in text_lower:
        return generate_surprise(lang)
    elif "цитата" in text_lower or "quote" in text_lower:
        return generate_quote(lang)
    elif "музика" in text_lower or "музыка" in text_lower or "music" in text_lower:
        return generate_music(lang)
    elif "фильм" in text_lower or "movie" in text_lower:
        return generate_movie(lang)
    elif "рандом" in text_lower or "random" in text_lower:
        return generate_random(lang)
    elif "рецепт" in text_lower or "recipe" in text_lower:
        return translate("🥕 Введіть список інгредієнтів через кому, і я знайду рецепти!", lang)
    else:
        return generate_surprise(lang)  # fallback вариант
