from modules.database import get_user, log_request
from datetime import datetime

MAX_REQUESTS_PER_DAY = 5

def check_limit(user_id):
    user = get_user(user_id)
    today = datetime.utcnow().date()
    count = sum(1 for t in user.get("requests", []) if datetime.fromisoformat(t).date() == today)
    return count < MAX_REQUESTS_PER_DAY

def register_request(user_id):
    log_request(user_id)
