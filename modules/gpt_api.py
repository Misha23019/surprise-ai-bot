import requests
import json
import os
import logging

API_KEY = os.getenv("OPENROUTER_API_KEY")  # Проверь, что переменная окружения установлена

logging.info(f"Using API key: {OPENROUTER_API_KEY[:5]}...")  # логируем первые 5 символов ключа

def ask_qwen(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # Можно указать свой URL сайта и название, если хочешь (опционально)
        # "HTTP-Referer": "https://example.com",
        # "X-Title": "My Surprise Bot",
    }
    data = {
        "model": "qwen/qwen3-235b-a22b:free",
        "messages": messages,
    }
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(data),
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
