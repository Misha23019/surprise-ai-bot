import requests
import json
import os
from modules.lang import get_prompt_template

def generate_response(user_input, lang):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    if not OPENROUTER_API_KEY:
        return "❌ API-ключ OpenRouter не знайдено. Зверніться до адміністратора."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # 🔤 Формуємо запит з урахуванням мови користувача
    prompt_template = get_prompt_template(lang)
    final_prompt = prompt_template.format(user_input=user_input)

    data = {
        "model": "qwen/qwen3-235b-a22b:free",
        "messages": [
            {"role": "user", "content": final_prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
            timeout=10
        )

        if response.status_code == 401:
            return "🚫 Невірний або недійсний API-ключ OpenRouter."
        elif response.status_code != 200:
            return f"❌ Помилка OpenRouter: {response.status_code} - {response.text}"

        response_data = response.json()
        message = response_data.get("choices", [{}])[0].get("message", {}).get("content")

        return message if message else "🤖 Відповідь порожня або не розпізнана."

    except requests.exceptions.Timeout:
        return "⏱️ Час очікування відповіді від AI вичерпано. Спробуйте ще раз."
    except Exception as e:
        return f"❌ Сталася помилка при підключенні до OpenRouter:\n{str(e)}"
