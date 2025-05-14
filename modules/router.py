import os
import requests
import json

OPENROUTER_API_KEY = "вставь_сюда_твой_ключ"  # Обязательно замени на свой

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://example.com",  # опционально
    "X-Title": "SurpriseMeBot",             # опционально
}

payload = {
    "model": "qwen/qwen3-235b-a22b:free",
    "messages": [
        {"role": "user", "content": "What is the meaning of life?"}
    ]
}
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "🤖 Вибач, не зміг згенерувати відповідь."
