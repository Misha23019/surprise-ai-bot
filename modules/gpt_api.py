import os
import requests

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def get_prompt(category, lang):
    prompts = {
        "Surprise": {
            "en": "Give me a random delightful surprise for today.",
            "uk": "Подаруй мені несподіваний приємний сюрприз на сьогодні."
        },
        "Movie": {
            "en": "Suggest a movie for tonight.",
            "uk": "Порекомендуй фільм на сьогоднішній вечір."
        },
        "Music": {
            "en": "Share a great song to listen to now.",
            "uk": "Поділись чудовою піснею для прослуховування."
        },
        "Quote": {
            "en": "Give me an inspiring quote.",
            "uk": "Надішли надихаючу цитату."
        },
        "Random": {
            "en": "Send me something random, fun and useful.",
            "uk": "Надішли щось випадкове, веселе та корисне."
        },
        "Recipe": {
            "en": "Give me a recipe using common ingredients.",
            "uk": "Порадь простий рецепт з доступних інгредієнтів."
        },
    }
    return prompts.get(category, {}).get(lang, prompts.get(category, {}).get("en"))

async def generate_content(category, lang):
    prompt = get_prompt(category, lang)
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {e}"
