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

    # ✅ Обработка команды /start
    if user_input == "/start":
        langs_list = "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()])
        send_message(chat_id, f"👋 Вітаю! Оберіть мову командою типу /lang uk\n\n🌐 Доступні мови:\n{langs_list}", TELEGRAM_TOKEN)
        return "OK", 200

    # ✅ Обработка команды /lang
    if user_input.startswith("/lang"):
        parts = user_input.split()
        if len(parts) == 2 and parts[1] in LANGUAGES:
            set_user_lang(chat_id, parts[1])
            send_message(chat_id, f"✅ Мова змінена на {LANGUAGES[parts[1]]}", TELEGRAM_TOKEN)
        else:
            langs_list = "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()])
            send_message(chat_id, "🌐 Виберіть мову (приклад: /lang uk):\n" + langs_list, TELEGRAM_TOKEN)
        return "OK", 200

    # ✅ Проверка лимита
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


