from modules.gpt_api import generate_gpt_response
from modules.limits import check_limit, increment_manual
from modules.lang import get_user_lang
import logging

def handle_message(chat_id, text):
    lang = get_user_lang(chat_id) or "uk"
    text_lower = text.lower()

    # Команды
    if text_lower == "/start":
        return (
            "👋 Вітаю! Оберіть мову командою типу /lang uk\n\n"
            "🌐 Доступні мови:\n"
            + "\n".join([f"{k} - {v}" for k, v in sorted(lang.LANGUAGES.items())])
        )

    if text_lower.startswith("/lang"):
        parts = text_lower.split()
        if len(parts) == 2 and parts[1] in lang.LANGUAGES:
            lang.set_user_lang(chat_id, parts[1])
            return lang.get_text(parts[1])["language_changed"]
        else:
            return "Невірний код мови. Спробуйте ще раз."

    # Ліміт на ручні запити
    if not check_limit(chat_id):
        return "❌ Ви досягли щоденного ліміту запитів (5). Спробуйте завтра."

    # Команди сюрприз, рецепт, рандом та ін.
    if text_lower == "🎲 сюрприз" or text_lower == "/auto_surprise":
        prompt = "Згенеруй короткий, цікавий сюрприз, який підніме настрій."
        response = generate_gpt_response(prompt, lang)
        increment_manual(chat_id)
        return response

    if text_lower == "🍽️ рецепт":
        return lang.get_text(lang)["ask_ingredients"]

    if text_lower.startswith("🥦") or "," in text_lower:  # інгредієнти
        # Беремо текст як список інгредієнтів
        ingredients = text
        prompt = f"Будь ласка, створи детальний рецепт страви, використовуючи ці інгредієнти: {ingredients}"
        response = generate_gpt_response(prompt, lang)
        increment_manual(chat_id)
        return response

    if text_lower == "🎬 фільм":
        prompt = "Порекомендуй цікавий фільм для перегляду."
        response = generate_gpt_response(prompt, lang)
        increment_manual(chat_id)
        return response

    if text_lower == "🎵 музика":
        prompt = "Порекомендуй хорошу пісню або альбом для прослуховування."
        response = generate_gpt_response(prompt, lang)
        increment_manual(chat_id)
        return response

    if text_lower == "💬 цитата":
        prompt = "Наведи надихаючу цитату."
        response = generate_gpt_response(prompt, lang)
        increment_manual(chat_id)
        return response

    if text_lower == "🔀 рандом":
        prompt = "Розкажи щось цікаве і випадкове."
        response = generate_gpt_response(prompt, lang)
        increment_manual(chat_id)
        return response

    # По замовчуванню - відповідь через GPT на будь-який текст
    response = generate_gpt_response(text, lang)
    increment_manual(chat_id)
    return response
