import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_gpt(prompt, model="qwen/qwen3-30b-a3b:free"):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()

    try:
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("GPT Error:", e, "\nFull response:", result)
        return "⚠️ Помилка генерації відповіді."

