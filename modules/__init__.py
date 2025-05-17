# modules/__init__.py

from .lang import get_text, get_all_languages, get_flag
from .limits import can_use, increase, reset_limits
from .gpt_api import ask_gpt
from .database import get_user, create_user, update_user
from .scheduler import schedule_daily_surprise
from .telegram import send_surprise, build_keyboard
from .router import handle_message
from .texts import default_texts  # если есть словарь/контент
