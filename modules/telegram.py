import requests
import json
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from modules.lang import get_text

def send_message(chat_id, text, token, keyboard=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if keyboard:
        # telegram API требует JSON строки в reply_markup
        payload["reply_markup"] = json.dumps(keyboard.to_dict())

    requests.post(url, json=payload)

def build_keyboard(lang_code):
    t = get_text(lang_code)
    keyboard = [
        [t["surprise"], t["movie"]],
        [t["music"], t["quote"]],
        [t["random"], t["recipe"]],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def build_inline_settings_keyboard(lang_code):
    t = get_text(lang_code)
    buttons = [
        [InlineKeyboardButton(t["change_lang"], callback_data="change_lang")],
        [InlineKeyboardButton(t["change_time"], callback_data="change_time")],
    ]
    return InlineKeyboardMarkup(buttons)
