import json
import os
import re
from modules.content import generate_surprise, generate_movie, generate_music, generate_quote, generate_random, generate_recipes
from modules.lang import get_text

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def generate_response(text, lang, chat_id):
    users = load_users()
    user_data = users.get(chat_id, {})

    # check for time format
    if re.fullmatch(r"[0-2]?\d:[0-5]\d", text):
        user_data["time"] = text
        users[chat_id] = user_data
        save_users(users)
        return get_text("time_saved", lang)

    # ask for time if not set
    if "time" not in user_data:
        return get_text("ask_time", lang)

    # handle recipe mode input
    if user_data.get("awaiting_ingredients"):
        user_data["awaiting_ingredients"] = False
        users[chat_id] = user_data
        save_users(users)
        return generate_recipes(text, lang)

    # command options
    lc = text.lower()
    if lc in ["🎲 сюрприз", "surprise"]:
        return generate_surprise(lang)
    if lc in ["🎬 фільм", "фильм", "movie"]:
        return generate_movie(lang)
    if lc in ["🎵 музика", "музыка", "music"]:
        return generate_music(lang)
    if lc in ["📜 цитата", "quote"]:
        return generate_quote(lang)
    if lc in ["🔀 рандом", "random"]:
        return generate_random(lang)
    if lc in ["🍳 рецепт", "рецепт", "recipe"]:
        user_data["awaiting_ingredients"] = True
        users[chat_id] = user_data
        save_users(users)
        return get_text("ask_ingredients", lang)

    return generate_surprise(lang)
