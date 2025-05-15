import requests
import json
from modules.lang import get_text

def send_message(chat_id, text, token, keyboard=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if keyboard:
        payload["reply_markup"] = json.dumps(keyboard)

    requests.post(url, json=payload)


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
