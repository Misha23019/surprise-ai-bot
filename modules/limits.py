from datetime import datetime, date
from modules.database import get_user, increment_manual_count_db, reset_manual_counts_if_needed_db

MAX_DAILY_MANUAL = 5  # Максимум ручных запросов в день

def can_send_manual(user_id: int) -> bool:
    """Проверяет, можно ли отправить ручной запрос."""
    reset_manual_counts_if_needed_db()  # Сброс лимитов если дата изменилась
    user = get_user(user_id)
    if not user:
        # Если пользователя нет — считаем, что можно (создание пользователя в другом месте)
        return True
    manual_count = user.get("manual_count", 0)
    return manual_count < MAX_DAILY_MANUAL

def register_manual_request(user_id: int):
    """Регистрирует ручной запрос (увеличивает счетчик)."""
    increment_manual_count_db(user_id)

def can_send_auto(user_id: int) -> bool:
    """Проверяет возможность отправки автосюрприза.
    В текущем варианте автосюрпризы не считаются в лимит,
    так что всегда возвращаем True."""
    return True
