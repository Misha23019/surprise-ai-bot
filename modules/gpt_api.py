import os
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

# Получаем API ключ из переменной окружения
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if OPENROUTER_API_KEY:
    logging.info(f"Using API key: {OPENROUTER_API_KEY[:5]}...")  # логируем первые 5 символов
else:
    logging.error("OPENROUTER_API_KEY is not set!")
    raise ValueError("OPENROUTER_API_KEY is not set!")

async def ask_qwen(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # Опционально:
        # "HTTP-Referer": "https://example.com",
        # "X-Title": "Surprise Me Bot",
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
