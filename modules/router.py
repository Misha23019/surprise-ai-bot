import requests
import json
import os
from modules.lang import get_prompt_template  # добавим шаблоны

def generate_response(user_input, lang):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # 🔤 Получаем шаблон и формируем финальный prompt
    prompt_template = get_prompt_template(lang)
    final_prompt = prompt_template.format(user_input=user_input)

    data = {
        "model": "qwen/qwen3-235b-a22b:free",
        "messages": [
            {"role": "user", "content": final_prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            if "choices" in response_data:
                return response_data["choices"][0]["message"]["content"]
            else:
                return "🤖 Відповідь порожня або незрозуміла."
        else:
            return f"❌ OpenRouter error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Помилка при підключенні до OpenRouter: {str(e)}"
