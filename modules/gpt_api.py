import os
import requests
import logging

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def generate_text(prompt, system_prompt=None, model="qwen/qwen3-30b-a3b:free", max_tokens=500):
    if not OPENROUTER_API_KEY:
        logging.error("OPENROUTER_API_KEY is not set in environment variables.")
        return "Ошибка: API ключ не настроен."

    payload = {
        "model": model,
        "messages": [],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 1,
        "stop": None
    }

    if system_prompt:
        payload["messages"].append({"role": "system", "content": system_prompt})

    payload["messages"].append({"role": "user", "content": prompt})

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        # Структура ответа может меняться, подстроим под OpenRouter
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return text.strip()
    except Exception as e:
        logging.error(f"GPT API request failed: {e}")
        return "Извините, произошла ошибка при генерации текста."

# Пример функций для конкретных типов контента

def generate_surprise_gpt(lang):
    prompt = {
        "en": "Give me a daily surprise message.",
        "uk": "Дай мені щоденне повідомлення-сюрприз.",
        # Добавить остальные языки по желанию
    }.get(lang, "Give me a daily surprise message.")

    return generate_text(prompt, system_prompt="You are a friendly bot that generates surprises.")

def generate_recipe_gpt(ingredients, lang):
    prompt = f"Provide 2-3 simple recipes using these ingredients: {', '.join(ingredients)}."
    return generate_text(prompt, system_prompt="You are a helpful cooking assistant.")
