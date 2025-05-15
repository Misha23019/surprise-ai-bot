def generate_recipe(ingredients, lang):
    items = [item.strip().capitalize() for item in ingredients.split(",") if item.strip()]

    if not items:
        return {
            "uk": "❌ Не вдалося розпізнати жодного інгредієнта.",
            "ru": "❌ Не удалось распознать ни одного ингредиента.",
            "en": "❌ No valid ingredients recognized."
        }.get(lang, "❌ No valid ingredients recognized.")

    recipe_text = {
        "uk": f"🍲 На основі: {', '.join(items)} — спробуйте зробити овочевий суп або салат!",
        "ru": f"🍲 Из: {', '.join(items)} — попробуйте приготовить овощной суп или салат!",
        "en": f"🍲 Based on: {', '.join(items)} — try making a vegetable soup or salad!"
    }

    return recipe_text.get(lang, recipe_text["en"])
