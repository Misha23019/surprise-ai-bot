# modules/__init__.py

# 🌐 Язык
from .lang import get_text, get_all_languages, get_flag

# 📊 Лимиты
from .limits import can_use, increase, reset_limits

# 🤖 GPT API
from .gpt_api import ask_gpt

# 🗃️ База данных
from .database import get_user, create_user, update_user

# ⏰ Планировщик
from .scheduler import schedule_daily_surprise

# 📩 Telegram
from .telegram import send_surprise, build_keyboard

# 🧭 Роутер
from .router import handle_message

# 📚 Тексты
from .texts import default_texts  # если default_texts — словарь/набор шаблонов
