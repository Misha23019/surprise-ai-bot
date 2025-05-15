from modules.telegram import send_message, build_keyboard, build_inline_settings_keyboard, build_lang_keyboard
from modules.lang import get_user_lang, set_user_lang, get_text, get_user_time, set_user_time
from modules.limits import check_limit, increment_manual, was_auto_sent, mark_auto_sent
from modules.gpt_api import ask_gpt

def handle_update(update, token):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        text = msg.get("text", "")

        user_lang = get_user_lang(user_id)
        texts = get_text(user_lang)

        # Команда /start или приветствие
        if text == "/start":
            send_message(chat_id, texts["start_choose_lang"], token)
            return

        # Смена языка через /lang xx
        if text.startswith("/lang "):
            lang_code = text.split(" ")[1]
            if lang_code in texts:
                set_user_lang(user_id, lang_code)
                send_message(chat_id, texts["language_changed"], token)
                send_message(chat_id, texts["ask_time"], token)
            else:
                send_message(chat_id, "❌ Unsupported language code.", token)
            return

        # Если пользователь еще не установил язык, просим выбрать
        if user_lang not in texts:
            send_message(chat_id, texts["start_choose_lang"], token, keyboard=build_lang_keyboard())
            return

        # Обработка выбора языка из инлайн-клавиатуры
        # (будет в callback_query, ниже)

        # Проверка лимитов
        if not check_limit(user_id):
            send_message(chat_id, "⚠️ You reached your daily limit of requests.", token)
            return

        # Основные команды через кнопки
        if text in [texts["surprise"], texts["movie"], texts["music"], texts["quote"], texts["random"], texts["recipe"]]:
            increment_manual(user_id)
            # Для примера, спросим GPT по тексту запроса:
            response = ask_gpt(text)
            send_message(chat_id, response, token, keyboard=build_keyboard(user_lang))
            return

        # Если пользователь вводит время
        if ":" in text and len(text) == 5:
            set_user_time(user_id, text)
            send_message(chat_id, f"✅ Time set to {text}", token, keyboard=build_keyboard(user_lang))
            return

        # Если пользователь вводит ингредиенты (пример)
        if text.count(",") >= 1:
            response = ask_gpt(f"Recipe with ingredients: {text}")
            send_message(chat_id, response, token, keyboard=build_keyboard(user_lang))
            return

        # По умолчанию — показать меню
        send_message(chat_id, "Please choose an option:", token, keyboard=build_keyboard(user_lang))

    elif "callback_query" in update:
        callback = update["callback_query"]
        data = callback["data"]
        chat_id = callback["message"]["chat"]["id"]
        user_id = callback["from"]["id"]
        user_lang = get_user_lang(user_id)
        texts = get_text(user_lang)

        if data.startswith("set_lang_"):
            lang_code = data.split("_")[-1]
            set_user_lang(user_id, lang_code)
            send_message(chat_id, texts["language_changed"], token)
            send_message(chat_id, texts["ask_time"], token)
            return

        if data == "change_lang":
            send_message(chat_id, texts["start_choose_lang"], token, keyboard=build_lang_keyboard())
            return

        if data == "change_time":
            send_message(chat_id, texts["ask_time"], token)
            return
