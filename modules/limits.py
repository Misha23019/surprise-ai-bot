from modules.database import get_user, increment_manual_count, reset_manual_counts_if_needed

MAX_DAILY_MANUAL = 5  # Максимум ручных запросов в день

def can_user_request(user_id: int) -> bool:
    """Проверяет, можно ли отправить ручной запрос."""
    reset_manual_counts_if_needed()  # Сбрасываем лимиты если дата изменилась
    user = get_user(user_id)
    if not user:
        return True
    manual_count = user.get("manual_count", 0)
    return manual_count < MAX_DAILY_MANUAL

def increment_manual_count_wrapper(user_id: int):
    """Регистрирует ручной запрос (увеличивает счетчик)."""
    increment_manual_count(user_id)

def can_send_auto(user_id: int) -> bool:
    """Автосюрпризы не считаются в лимитах — всегда True."""
    return True
