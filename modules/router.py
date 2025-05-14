import requests
import json
import os

def generate_response(user_input):
    # Получаем API ключ из окружения
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # Заголовки для запроса
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Формируем данные для запроса
    data = {
        "model": "qwen/qwen3-235b-a22b:free",  # Убедитесь, что модель подходит для вашего запроса
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    # Отправляем запрос к API OpenRouter
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            # Если статус 200, парсим ответ
            response_data = response.json()
            if "choices" in response_data:
                # Возвращаем ответ от модели
                return response_data["choices"][0]["message"]["content"]
            else:
                return "🤖 Відповідь порожня або незрозуміла."
        else:
            return f"❌ OpenRouter error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Помилка при підключенні до OpenRouter: {str(e)}"
