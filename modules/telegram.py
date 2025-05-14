import requests

def send_message(chat_id, text, token, keyboard=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if keyboard:
        payload["reply_markup"] = {"keyboard": keyboard, "resize_keyboard": True}
    requests.post(url, json=payload)

def build_keyboard(lang="uk"):
    return [
        [{"text": "🎲 Сюрприз"}, {"text": "🎥 Фільм"}],
        [{"text": "🎧 Музика"}]
    ]
