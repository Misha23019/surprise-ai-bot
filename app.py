from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import random
import json
import datetime

# Загружаем переменные окружения
load_dotenv()

# Загрузка ключей из .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not TELEGRAM_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("❌ Не знайдено необхідних API ключів!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

app = Flask(__name__)

# Геолокация
geolocator = Nominatim(user_agent="surprise-bot")
tf = TimezoneFinder()

# Пользовательские данные в памяти
user_data = {}  # chat_id: {"location": ..., "timezone": ...}

# Контент для ежедневных постов
content_list = [
    "🎬 Рандомний фільм",
    "🎷 Музика",
    "📚 Цитата або уривок з книги",
    "🌐 Маловідомий сайт",
    "🧠 Цікавий факт",
    "😂 Жарт / цитата",
    "🕵️ Містичний контент",
    "🖼️ Твір мистецтва з описом",
    "🎷 Подкаст або YouTube-канал",
    "🎯 Щоденне завдання",
    "🧵 Коротка історія",
    "💭 Тема дня",
    "Рецепт для приготування",
]

# Отправка контента
def send_random_post(chat_id):
    content = random.choice(content_list)
    response = requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": content})
    print(f"[✉️] {datetime.datetime.now()} Пост відправлено: {content}")

# Планирование постов
scheduler = BackgroundScheduler()

def schedule_user_message(chat_id, tz):
    scheduler.add_job(
        send_random_post,
        'cron',
        hour=10, minute=0,
        timezone=timezone(tz),
        args=[chat_id],
        id=str(chat_id),
        replace_existing=True
    )

scheduler.start()

# Генерация ответа от OpenRouter
def generate_response(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen/qwen3-32b:free",
        "messages": [{"role": "user", "content": user_input}]
    }
    response = requests.post(OPENROUTER_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        res = response.json()
        return res["choices"][0]["message"]["content"]
    return "🤖 Вибач, не зміг згенерувати відповідь."

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "❌ Невірний формат", 400

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if chat_id not in user_data:
        tz = get_timezone_from_location(text)
        if tz:
            user_data[chat_id] = {"location": text, "timezone": tz}
            schedule_user_message(chat_id, tz)
            reply = f"✅ Щоденне повідомлення буде приходити о 10:00 ({tz})"
        else:
            reply = "🌍 Введи назву міста або країни для розсилки."
    else:
        reply = generate_response(text)

    # Клавіатура
    keyboard = {
        "keyboard": [
            [{"text": "🎲 Сюрприз"}, {"text": "🎬 Фільм"}],
            [{"text": "🎷 Музика"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

    requests.post(TELEGRAM_API_URL, json={
        "chat_id": chat_id,
        "text": reply,
        "reply_markup": keyboard
    })

    return "OK", 200

def get_timezone_from_location(location_name):
    location = geolocator.geocode(location_name)
    if location:
        return tf.timezone_at(lng=location.longitude, lat=location.latitude)
    return None

@app.route("/")
def home():
    return "✅ SurpriseBot працює!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
