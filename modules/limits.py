from datetime import datetime
from modules.database import get_user, update_user

async def is_allowed(user_id):
    user = await get_user(user_id)
    today = str(datetime.utcnow().date())
    if user["last_reset"] != today:
        await update_user(user_id, {"limit": 5, "last_reset": today})
        return True
    return user["limit"] > 0

async def decrease_limit(user_id):
    user = await get_user(user_id)
    new_limit = max(0, user["limit"] - 1)
    await update_user(user_id, {"limit": new_limit})
