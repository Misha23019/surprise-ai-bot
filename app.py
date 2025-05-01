from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Завантаження змінних з .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not TELEGRAM_TOKEN or not HUGGINGFACE_API_KEY:
    raise ValueError("❌ Не знайдено необхідних API ключів!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"

app = Flask(__name__)

# Функція для генерації відповіді через HuggingFace
def generate_response(prompt):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    data = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 50}
    }

    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data, list) and "generated_text" in response_data[0]:
            return response_data[0]["generated_text"]
        elif isinstance(response_data, list) and "generated_text" not in response_data[0] and "output" in response_data[0]:
            return response_data[0]["output"]
        else:
            return response_data[0] if isinstance(response_data[0], str) else str(response_data)
    else:
        print(f"❌ Помилка від HuggingFace: {response.status_code} - {response.text}")
        return "🤖 Вибач, не зміг згенерувати відповідь."

@app.route("/")
def home():
    return "✅ SurpriseBot працює без Ollama!"

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "❌ Невірний формат", 400

    chat_id = data["message"]["chat"]["id"]
    user_input = data["message"].get("text", "")

    if user_input:
        reply = generate_response(user_input)

        # Клавіатура для Telegram
        keyboard = {
            "keyboard": [
                [{"text": "🎲 Сюрприз"}, {"text": "🎥 Фільм"}],
                [{"text": "🎧 Музика"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }

        # Відправка відповіді в Telegram
        response = requests.post(TELEGRAM_API_URL, json={
            "chat_id": chat_id,
            "text": reply,
            "reply_markup": keyboard
        })

        print(f"📨 Відповідь надіслана: {reply}")
        print("📤 Telegram API статус:", response.status_code)

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
