from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Завантаження змінних з .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не знайдено в середовищі!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

app = Flask(__name__)

# Простий генератор відповіді
def generate_response(prompt):
    responses = {
        "🎲 Сюрприз": "😲 Твій сюрприз: пончик, який ніколи не закінчується!",
        "🎥 Фільм": "🎬 Подивись: Everything Everywhere All at Once (2022)",
        "🎧 Музика": "🎵 Спробуй послухати: 'Tame Impala – The Less I Know the Better'"
    }
    return responses.get(prompt, f"🤖 Ти написав: {prompt}")

@app.route("/")
def home():
    return "✅ SurpriseBot працює без Ollama!"

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "❌ Невірний формат", 400

    chat_id = data["message"]["chat"]["id"]
    user_input = data["message"].get("text", "")

    if user_input:
        reply = generate_response(user_input)

        keyboard = {
            "keyboard": [
                [{"text": "🎲 Сюрприз"}, {"text": "🎥 Фільм"}],
                [{"text": "🎧 Музика"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }

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
