from flask import Flask, request
from dotenv import load_dotenv
import os
import requests

from modules.router import handle_message
from modules.telegram import send_message, build_keyboard, build_lang_keyboard
from modules.scheduler import start_scheduler
from modules.limits import check_limit, increment_manual
from modules.lang import get_user_lang, set_user_lang, LANGUAGES, get_user_time, set_user_time

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не знайдено в .env")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ SurpriseBot працює!"

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data:
        return "❌ Невірний формат", 400

    # Обробка callback_query (натискання кнопок)
    if "callback_query" in data:
        callback = data["callback_query"]
        chat_id = str(callback["from"]["id"])
        data_str = callback.get("data", "")

        if data_str.startswith("set_lang_"):
            lang_code = data_str.replace("set_lang_", "")
            if lang_code in LANGUAGES:
                set_user_lang(chat_id, lang_code)
                send_message(chat_id, f"✅ Мова змінена на {LANGUAGES[lang_code]}", TELEGRAM_TOKEN)
            else:
                send_message(chat_id, "❌ Невідома мова", TELEGRAM_TOKEN)

            # Відповідь на callback_query, щоб прибрати "loading"
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
                json={"callback_query_id": callback.get("id")}
            )
            return "OK", 200

    # Обробка звичайних повідомлень
    if "message" not in data:
        return "❌ Невірний формат", 400

    message = data["message"]
    chat_id = str(message["chat"]["id"])
    user_input = message.get("text", "").strip()
    lang = get_user_lang(chat_id)
    user_time = get_user_time(chat_id)

    # Команда /start — надсилаємо клавіатуру з кнопками мов
    if user_input.startswith("/start"):
        send_message(
            chat_id,
            "👋 Вітаю! Оберіть мову, натиснувши кнопку нижче:",
            TELEGRAM_TOKEN,
            keyboard=build_lang_keyboard()
        )
        return "OK", 200

    # Команда /lang — встановлення мови (альтернативний спосіб)
    if user_input.startswith("/lang"):
        parts = user_input.split()
        if len(parts) == 2 and parts[1] in LANGUAGES:
            set_user_lang(chat_id, parts[1])
            send_message(
                chat_id,
                f"✅ Мова змінена на {LANGUAGES[parts[1]]}\n⌚ Введіть поточний час у форматі ГГ:ХХ (наприклад, 09:30), щоб отримувати сюрприз о 10:00",
                TELEGRAM_TOKEN
            )
        else:
            langs_list = "\n".join([f"{k} - {v}" for k, v in LANGUAGES.items()])
            send_message(
                chat_id,
                "🌐 Виберіть мову (приклад: /lang uk):\n" + langs_list,
                TELEGRAM_TOKEN
            )
        return "OK", 200

    # Якщо мову ще не обрано
    if not lang:
        send_message(chat_id, "🌐 Спочатку оберіть мову командою типу /start", TELEGRAM_TOKEN)
        return "OK", 200

    # Якщо час ще не заданий
    if not user_time:
        if ":" in user_input:
            # Валідація формату часу ГГ:ХХ (наприклад, 09:30)
            time_parts = user_input.split(":")
            if len(time_parts) == 2 and all(p.isdigit() for p in time_parts):
                hours, minutes = map(int, time_parts)
                if 0 <= hours <= 23 and 0 <= minutes <= 59:
                    set_user_time(chat_id, user_input)
                    send_message(chat_id, "✅ Час збережено! Оберіть одну з опцій нижче:", TELEGRAM_TOKEN, build_keyboard(lang))
                    return "OK", 200

            send_message(chat_id, "❌ Невірний формат часу. Введіть у форматі ГГ:ХХ (наприклад, 09:30)", TELEGRAM_TOKEN)
        else:
            send_message(chat_id, "⌚ Введіть поточний час у форматі ГГ:ХХ (наприклад, 09:30)", TELEGRAM_TOKEN)
        return "OK", 200

    # Перевірка ліміту
    if not check_limit(chat_id):
        send_message(chat_id, "⚠️ Ви досягли ліміту в 5 запитів на день. Спробуйте завтра!", TELEGRAM_TOKEN)
        return "OK", 200

    # Основна логіка
    reply = handle_message(chat_id, user_input)
    increment_manual(chat_id)
    send_message(chat_id, reply, TELEGRAM_TOKEN, build_keyboard(lang))

    return "OK", 200


if __name__ == "__main__":
    start_scheduler()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
