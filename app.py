from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
from langdetect import detect
import googletrans
from googletrans import Translator

load_dotenv()  # Завантаження змінних з .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Можно оставить имя переменной как есть

if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("❌ Не знайдено необхідних API ключів!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

app = Flask(__name__)
translator = Translator()

# Функція генерації відповіді через OpenRouter
def generate_response(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "SurpriseMeBot"
    }

    # Определяем язык пользователя
    lang = detect(user_input)

    if lang == "uk":
        system_message = "Ти — креативний асистент, який відповідає українською, весело й неочікувано."
    elif lang == "ru":
        system_message = "Ты — креативный ассистент, который отвечает по-русски, весело и неожиданно."
    else:
        system_message = "You are a creative assistant who replies in English with weird, fun, unexpected ideas."

    # Определяем prompt
    if "фільм" in user_input.lower() or "🎥" in user_input:
        prompt = "Запропонуй дивну й неочікувану назву фільму з одним смішним описом."
    elif "музика" in user_input.lower() or "🎧" in user_input:
        prompt = "Запропонуй дивний музичний жанр або гурт з незвичним описом."
    elif "сюрприз" in user_input.lower() or "🎲" in user_input:
        prompt = "Придумай випадкову, дивну ідею-сюрприз у 1–2 реченнях."
    else:
        prompt = user_input  # Используем оригинальный текст

    data = {
        "model": "qwen/qwen3-32b:free",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1.0
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        print("✅ OpenRouter response:", response_data)
        return response_data["choices"][0]["message"]["content"]
    else:
        print(f"❌ OpenRouter error: {response.status_code} - {response.text}")
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
