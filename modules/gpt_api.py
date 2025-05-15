import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_gpt_response(prompt, lang="uk"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    messages = [
        {"role": "system", "content": f"You are a helpful assistant speaking in {lang}."},
        {"role": "user", "content": prompt}
    ]
    payload = {
        "model": "gpt-4o-mini",  # или нужная модель
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        return "Вибачте, сталася помилка при генерації відповіді."
