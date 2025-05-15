import os
import requests
import json

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def query_gpt(prompt, model="qwen/qwen3-30b-a3b:free", temperature=0.7):
    if not OPENROUTER_API_KEY:
        raise Exception("OPENROUTER_API_KEY не установлен в окружении")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
    }

    response = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        raise Exception(f"Ошибка API: {response.status_code} {response.text}")

    resp_json = response.json()
    return resp_json["choices"][0]["message"]["content"]
