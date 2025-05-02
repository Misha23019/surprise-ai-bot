from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
from langdetect import detect
import googletrans
from googletrans import Translator

load_dotenv()  # Завантаження змінних з .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not TELEGRAM_TOKEN or not HUGGINGFACE_API_KEY:
    raise ValueError("❌ Не знайдено необхідних API ключів!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

app = Flask(__name__)
translator = Translator()

# Функція генерації відповіді через HuggingFace
def generate_response(user_input):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    # Визначаємо тип запиту
    if "фільм" in user_input.lower() or "🎥" in user_input:
        prompt = "Suggest a weird and random movie title with a one-line funny description."
    elif "музика" in user_input.lower() or "🎧" in user_input:
        prompt = "Suggest a bizarre and unexpected music genre or band with a strange description."
    elif "сюрприз" in user_input.lower() or "🎲" in user_input:
        prompt = "Give a weird, random, AI-generated surprise idea in 1–2 sentences."
    else:
        prompt = f"Respond with a funny and strange idea based on: {user_input}"

    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 1.3,
            "top_k": 50,
            "top_p": 0.95,
            "repetition_penalty": 1.3
        }
    }

    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=data)

   if response.status_code == 200:
        response_data = response.json()
        print("✅ HuggingFace response:", response_data)

        # Перевіряємо структуру
        if isinstance(response_data, dict) and "generated_text" in response_data:
            return response_data["generated_text"]
        elif isinstance(response_data, list) and "generated_text" in response_data[0]:
            return response_data[0]["generated_text"]
        elif isinstance(response_data, dict) and "data" in response_data:
            return response_data["data"]
        else:
            return "🤖 Відповідь порожня або незрозуміла."
    else:
        print(f"❌ HuggingFace error: {response.status_code} - {response.text}")
        print("📛 HuggingFace відповідь:", response.text)
        return "🤖 Вибач, не зміг згенерувати відповідь."


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

@app.route("/")
def home():
    return "✅ SurpriseBot працює і чекає Telegram-запити!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
