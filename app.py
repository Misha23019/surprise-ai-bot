from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import random
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Загружаем переменные окружения
load_dotenv()

# Ключи API
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("❌ Не знайдено необхідних API ключів!")

# Настройки API
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

app = Flask(__name__)

# Память ограничений: сколько запросов сделал каждый пользователь (обнуляется каждый день)
user_limits = defaultdict(lambda: {"count": 0, "reset": datetime.utcnow().date()})

# Контент для ежедневного поста
content_list = [
    "🎬 Рандомний фільм", "🎧 Музика", "📚 Цитата з книги",
    "🌐 Маловідомий сайт", "🧠 Цікавий факт", "😂 Жарт",
    "🕵️ Містичний контент", "🖼️ Твір мистецтва", "🎙️ Подкаст",
    "🎯 Щоденне завдання", "🧵 Коротка історія", "💭 Тема дня",
    "🍳 Рецепт для приготування"
]

# --- ЯЗЫКОВАЯ ПОДДЕРЖКА ---
def get_prompt(user_input, lang="uk"):
    text = user_input.lower()
    if "фільм" in text or "🎥" in text:
        return "Запропонуй дивну й неочікувану назву фільму з одним смішним описом." if lang == "uk" else \
               "Suggest a weird and unexpected movie title with a funny description."
    elif "музика" in text or "🎧" in text:
        return "Запропонуй дивний музичний жанр або гурт з незвичним описом." if lang == "uk" else \
               "Suggest a bizarre music genre or band with a strange description."
    elif "сюрприз" in text or "🎲" in text:
        return "Придумай випадкову, дивну ідею-сюрприз у 1–2 реченнях." if lang == "uk" else \
               "Create a random, weird surprise idea in 1–2 sentences."
    else:
        return user_input

# --- ГЕНЕРАЦИЯ ВІДПОВІДІ ---
def generate_response(user_input, lang="uk"):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = get_prompt(user_input, lang)
    data = {
        "model": "qwen/qwen3-32b:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        if "choices" in response_data:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "🤖 Відповідь порожня або незрозуміла."
    else:
        return "🤖 Вибач, не зміг згенерувати відповідь."

# --- ОТПРАВКА РАНДОМНОГО ПОСТА ---
def send_random_post():
    random_content = random.choice(content_list)
    chat_id = "<YOUR_CHAT_ID>"  # Заміни на свій ID
    response = requests.post(TELEGRAM_API_URL, json={
        "chat_id": chat_id,
        "text": random_content
    })

# --- ПЛАНУВАЛЬНИК ---
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_random_post, 'interval', days=1, start_date='2025-05-15 10:00:00')  # 10:00 по UTC
    scheduler.start()

# --- ВЕБХУК ДЛЯ ТЕЛЕГРАМ ---
@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "❌ Невірний формат", 400

    chat_id = data["message"]["chat"]["id"]
    user_input = data["message"].get("text", "")

    # Ограничение по количеству запросов
    today = datetime.utcnow().date()
    user_data = user_limits[chat_id]

    if user_data["reset"] < today:
        user_limits[chat_id] = {"count": 0, "reset": today}
        user_data = user_limits[chat_id]

    if user_data["count"] >= 5:
        msg = "⚠️ Ви досягли ліміту на 5 запитів за день. Повторіть завтра."
        requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": msg})
        return "LIMIT", 200

    reply = generate_response(user_input, lang="uk")
    user_limits[chat_id]["count"] += 1

    # Клавіатура Telegram
    keyboard = {
        "keyboard": [
            [{"text": "🎲 Сюрприз"}, {"text": "🎥 Фільм"}],
            [{"text": "🎧 Музика"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

    # Відправка
    requests.post(TELEGRAM_API_URL, json={
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": keyboard
    })

    return "OK", 200

@app.route("/")
def home():
    return "✅ SurpriseBot працює і чекає Telegram-запити!"

if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=10000)
