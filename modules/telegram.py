import requests
import json
from modules.lang import get_text, LANGUAGES  # додано LANGUAGES

def send_message(chat_id, text, token, keyboard=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)

    try:
        response = requests.post(url, json=payload)
        if not response.ok:
            print(f"❌ Помилка при відправці повідомлення в Telegram: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"❌ Помилка мережі при відправці повідомлення: {e}")


def build_keyboard(lang_code):
    t = get_text(lang_code)
    return {
        "keyboard": [
            [ {"text": t["surprise"]}, {"text": t["movie"]} ],
            [ {"text": t["music"]}, {"text": t["quote"]} ],
            [ {"text": t["random"]}, {"text": t["recipe"]} ]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


def build_inline_settings_keyboard(lang_code):
    t = get_text(lang_code)
    return {
        "inline_keyboard": [
            [ {"text": t["change_lang"], "callback_data": "change_lang"} ],
            [ {"text": t["change_time"], "callback_data": "change_time"} ]
        ]
    }

def build_lang_keyboard():
    buttons = []
    langs = list(LANGUAGES.items())
    row = []
    for i, (code, name) in enumerate(langs, 1):
        row.append({"text": name, "callback_data": f"set_lang_{code}"})
        if i % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    return {
        "inline_keyboard": buttons
    }
