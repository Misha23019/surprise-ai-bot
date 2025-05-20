# modules/__init__.py

# 🌐 Язык
from .lang import get_text, ask_language, ask_time
from .languages import LANGUAGES, get_flag

# 📊 Лимиты
from .limits import can_use, increase, reset_limits

# 🤖 GPT API
from .gpt_api import ask_gpt

# 🗃️ База данных
from .database import get_user, update_user, save_user, save_language

# ⏰ Планировщик
from .scheduler import schedule_daily_surprise, start_scheduler

# 📩 Telegram
from .telegram import send_surprise, build_keyboard, setup_handlers

# 🧭 Роутер
from .router import router as main_router  # 👈 используем router как main_router

# 📚 Тексты
from .texts import default_texts

# 🪄 Контент
from .content import generate_content_from_message, generate_content_from_text
