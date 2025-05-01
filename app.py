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
def generate_response(prompt):
    try:
        lang = detect(prompt)
        if lang != "en":
            prompt = translator.translate(prompt, src=lang, dest="en").text
    except Exception as e:
        print("⚠️ Помилка визначення або перекладу мови:", e)

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    full_prompt = f"Give me a short, weird AI-generated surprise:\n{prompt}"

    data = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 1.3,
            "top_k": 50,
            "top_p": 0.95,
            "repetition_penalty": 1.4
        }
    }

    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data, list) and len(response_data) > 0:
            generated_text = response_data[0]["generated_text"]
            # Очистити prompt з відповіді
            if full_prompt in generated_text:
                cleaned = generated_text.replace(full_prompt, "").strip()
            else:
                cleaned = generated_text.strip()
            return cleaned
        else:
            return "🤖 Відповіді немає або вона пуста."
    else:
        print(f"❌ HuggingFace error: {response.status_code} - {response.text}")
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
