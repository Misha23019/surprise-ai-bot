import requests

def send_message(chat_id, text, token, keyboard=None, inline_keyboard=None):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    if keyboard:
        payload["reply_markup"] = {"keyboard": keyboard, "resize_keyboard": True}

    if inline_keyboard:
        payload["reply_markup"] = {
            "inline_keyboard": inline_keyboard
        }

    requests.post(url, json=payload)

def build_keyboard(lang="uk"):
    return [
        [{"text": "🎲 Сюрприз"}, {"text": "🎥 Фільм"}],
        [{"text": "🎧 Музика"}, {"text": "📜 Цитата"}],
        [{"text": "🔀 Рандом"}, {"text": "🍳 Рецепт"}]
    ]

def build_settings_inline():
    return [
        [
            {"text": "🌐 Змінити мову", "callback_data": "change_language"},
            {"text": "⏰ Змінити час", "callback_data": "change_time"}
        ]
    ]
