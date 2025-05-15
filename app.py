### app.py ###

from flask import Flask, request
from dotenv import load_dotenv
import os
from modules.router import generate_response
from modules.telegram import send_message, build_keyboard, build_inline_settings_keyboard
from modules.scheduler import start_scheduler
from modules.limits import check_limit, increment_limit
from modules.lang import get_user_lang, set_user_lang, LANGUAGES, get_user_time, set_user_time, get_text
import re

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в .env")

app = Flask(__name__)

TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")  # Формат HH:MM

@app.route("/")
def home():
    return "✅ SurpriseBot працює!"

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data:
        return "❌ Невірний формат", 400

    # Обработка callback_query для inline-кнопок (смена языка и времени)
    if "callback_query" in data:
        callback = data["callback_query"]
        chat_id = str(callback["message"]["chat"]["id"])
        lang = get_user_lang(chat_id)
        data_cb = callback["data"]

        if data_cb == "change_lang":
            langs_list = "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()])
            send_message(chat_id, f"🌐 Виберіть мову (приклад: /lang uk):\n{langs_list}", TELEGRAM_TOKEN)
            # Можно установить какой-то state, чтобы ждать ввода /lang ...
            return "OK", 200

        elif data_cb == "change_time":
            t = get_text(lang)
            send_message(chat_id, t["ask_time"], TELEGRAM_TOKEN)
            # Аналогично, можно ждать ввода времени от пользователя
            return "OK", 200

        return "OK", 200

    if "message" not in data:
        return "❌ Невірний формат", 400

    message = data["message"]
    chat_id = str(message["chat"]["id"])
    user_input = message.get("text", "").strip()

    lang = get_user_lang(chat_id)
    user_time = get_user_time(chat_id)

    if user_input.startswith("/start"):
        langs_list = "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()])
        send_message(chat_id, f"👋 Вітаю! Оберіть мову командою типу /lang uk\n\n🌐 Доступні мови:\n{langs_list}", TELEGRAM_TOKEN)
        return "OK", 200

    if user_input.startswith("/lang"):
        parts = user_input.split()
        if len(parts) == 2 and parts[1] in LANGUAGES:
            set_user_lang(chat_id, parts[1])
            t = get_text(parts[1])
            send_message(chat_id, f"✅ {t['language_changed']}\n{t['ask_time']}", TELEGRAM_TOKEN)
        else:
            langs_list = "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()])
            send_message(chat_id, "🌐 Виберіть мову (приклад: /lang uk):\n" + langs_list, TELEGRAM_TOKEN)
        return "OK", 200

    if not lang:
        send_message(chat_id, "🌐 Спочатку оберіть мову командою типу /lang uk", TELEGRAM_TOKEN)
        return "OK", 200

    if not user_time:
        # Проверяем формат времени
        if TIME_PATTERN.match(user_input):
            set_user_time(chat_id, user_input)
            t = get_text(lang)
            send_message(chat_id, "✅ " + t["ask_time"], TELEGRAM_TOKEN)
            # После сохранения времени показываем главное меню с кнопками
            keyboard = build_keyboard(lang)
            send_message(chat_id, "Обирайте опцію:", TELEGRAM_TOKEN, keyboard)
        else:
            t = get_text(lang)
            send_message(chat_id, t["ask_time"], TELEGRAM_TOKEN)
        return "OK", 200

    # Проверяем лимит запросов
    if not check_limit(chat_id):
        send_message(chat_id, "⚠️ Ви досягли ліміту в 5 запитів на день. Спробуйте завтра!", TELEGRAM_TOKEN)
        return "OK", 200

    # Генерируем ответ по команде
    reply = generate_response(user_input, lang)
    increment_limit(chat_id)
    keyboard = build_keyboard(lang)
    send_message(chat_id, reply, TELEGRAM_TOKEN, keyboard)

    return "OK", 200

if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=10000)
