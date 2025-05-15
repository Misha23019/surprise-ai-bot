def handle_message(user_id, text):
    user_id = str(user_id)

    lang = user_states.get(user_id, {}).get("lang", get_user_lang(user_id))
    texts = get_text(lang)

    state = user_states.get(user_id, {}).get("state")

    if state == "await_time":
        if validate_time_format(text):
            set_user_time(user_id, text)
            user_states[user_id]["state"] = None
            return f"⏰ {texts['change_time']} збережено: {text}. Дякуємо!"
        else:
            return "❌ Невірний формат часу. Введіть у форматі ГГ:ХХ (наприклад, 09:30)."

    if state == "await_ingredients":
        user_states[user_id]["state"] = None
        prompt = (
            f"Будь ласка, створи детальний рецепт страви, використовуючи ці інгредієнти: {text}"
            if lang == "uk"
            else f"Please create a detailed recipe using these ingredients: {text}"
        )
        return generate_gpt_response(prompt, lang)  # ✅ Додано return і функція завершиться тут

    if text.startswith("/lang "):
        new_lang = text.split(" ", 1)[1].strip()
        if new_lang in get_text(new_lang):
            set_user_lang(user_id, new_lang)
            user_states[user_id] = {"state": None, "lang": new_lang}
            texts = get_text(new_lang)
            return f"✅ {texts['language_changed']}\n\n{texts['ask_time']}"
        else:
            return "❌ Unsupported language code."

    if text == texts["change_time"]:
        user_states[user_id] = {"state": "await_time", "lang": lang}
        return texts["ask_time"]

    if text == texts["change_lang"]:
        user_states[user_id]["state"] = None
        return texts["start_choose_lang"]

    text_lower = text.lower()

    if any(word in text_lower for word in [texts["surprise"].lower(), "сюрприз", "surprise"]):
        prompt = (
            "Створи короткий, цікавий сюрприз українською"
            if lang == "uk"
            else "Create a short, interesting surprise in English"
        )
        return generate_gpt_response(prompt, lang)

    if any(word in text_lower for word in [texts["quote"].lower(), "цитата", "quote"]):
        prompt = (
            "Наведи надихаючу цитату українською"
            if lang == "uk"
            else "Provide an inspiring quote in English"
        )
        return generate_gpt_response(prompt, lang)

    if any(word in text_lower for word in [texts["music"].lower(), "музика", "музыка", "music"]):
        prompt = (
            "Порадь популярну пісню українською"
            if lang == "uk"
            else "Recommend a popular song in English"
        )
        return generate_gpt_response(prompt, lang)

    if any(word in text_lower for word in [texts["movie"].lower(), "фільм", "фильм", "movie"]):
        prompt = (
            "Порадь цікавий фільм українською"
            if lang == "uk"
            else "Recommend an interesting movie in English"
        )
        return generate_gpt_response(prompt, lang)

    if any(word in text_lower for word in [texts["random"].lower(), "рандом", "random"]):
        return generate_random(lang)

    if any(word in text_lower for word in [texts["recipe"].lower(), "рецепт", "recipe"]):
        user_states[user_id] = {"state": "await_ingredients", "lang": lang}
        return texts["ask_ingredients"]

    return generate_surprise(lang)
