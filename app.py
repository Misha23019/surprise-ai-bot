from flask import Flask, request
from dotenv import load_dotenv
import os
from modules.router import generate_response
from modules.telegram import send_message, build_keyboard
from modules.scheduler import start_scheduler
from modules.limits import check_limit, increment_limit
from modules.lang import get_user_lang, set_user_lang, LANGUAGES

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в .env")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ SurpriseBot працює!"

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "❌ Невірний формат", 400

    chat_id = str(data["message"]["chat"]["id"])
    user_input = data["message"].get("text", "")

    if user_input.startswith("/lang"):
        parts = user_input.split()
        if len(parts) == 2 and parts[1] in LANGUAGES:
            set_user_lang(chat_id, parts[1])
            send_message(chat_id, f"✅ Мова змінена на {LANGUAGES[parts[1]]}", TELEGRAM_TOKEN)
        else:
            langs_list = "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()])
            send_message(chat_id, "🌐 Виберіть мову (приклад: /lang uk):\n" + langs_list, TELEGRAM_TOKEN)
        return "OK", 200

    if not check_limit(chat_id):
        send_message(chat_id, "⚠️ Ви досягли ліміту в 5 запитів на день. Спробуйте завтра!", TELEGRAM_TOKEN)
        return "OK", 200

    lang = get_user_lang(chat_id)
    reply = generate_response(user_input, lang)
    increment_limit(chat_id)
    keyboard = build_keyboard(lang)
    send_message(chat_id, reply, TELEGRAM_TOKEN, keyboard)

    return "OK", 200

if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=10000)

# 📁 requirements.txt
flask
requests
python-dotenv
apscheduler

# 📁 README.md

# Surprise Me! Telegram Bot

#🎉 Бот, що щодня надсилає сюрпризи: фільми, музику, мистецтво, факти тощо.

## ✨ Функціональність
- 🚀 Щоденні автоматичні пости
- 🤓 Генерація відповідей через OpenRouter
- ⚠️ Обмеження: 5 запитів на день
- 🌐 Мультимовність (25+ мов)
- ⌨п Можливість змінити мову: `/lang uk`, `/lang en` тощо

## 📊 Технології
- Flask + Telegram Webhook
- OpenRouter API (LLM)
- APScheduler для авто-розсилки

## 🔍 Приклад .env
```
TELEGRAM_TOKEN=тут_токен_бота
OPENROUTER_API_KEY=тут_ключ_OpenRouter
```

## 🚀 Деплой на Render
- Завантаж репозиторій на GitHub
- Створи Web Service на https://render.com
- Build Command: `pip install -r requirements.txt`
- Start Command: `python app.py`
- Додай ENV:
  - TELEGRAM_TOKEN
  - OPENROUTER_API_KEY
