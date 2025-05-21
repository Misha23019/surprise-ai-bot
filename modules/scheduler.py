# modules/scheduler.py
import asyncio
from datetime import datetime
import aiosqlite
import logging

from modules.content import generate_scheduled_content
from modules.database import init_db

DB_PATH = "db.sqlite3"
sent_users = set()

async def start_scheduler():
    """
    Запускает бесконечный цикл планировщика,
    который каждую минуту проверяет, кому нужно отправить сюрприз.
    """
    logging.info("⏰ Планировщик запущен")
    
    while True:
        now_utc = datetime.utcnow().strftime("%H:%M")  # Время в формате "ЧЧ:ММ" UTC

        # Инициализация базы данных — на всякий случай, чтобы таблицы были готовы
        try:
            await init_db()
        except Exception as e:
            logging.error(f"Ошибка инициализации базы данных в планировщике: {e}")
            await asyncio.sleep(60)
            continue

        try:
            async with aiosqlite.connect(DB_PATH) as db:
                async with db.execute("SELECT user_id, time, lang FROM users") as cursor:
                    async for user_id, user_time, lang in cursor:
                        # Значения по умолчанию
                        user_time = user_time or "10:00"
                        lang = lang or "en"

                        if now_utc == user_time:
                            if user_id not in sent_users:
                                try:
                                    await generate_scheduled_content(user_id, lang)
                                    logging.info(f"✅ Отправлен сюрприз пользователю {user_id} в {now_utc} UTC")
                                except Exception as e:
                                    logging.error(f"Ошибка при отправке сюрприза пользователю {user_id}: {e}")
                                else:
                                    sent_users.add(user_id)
                        else:
                            # Если время не совпадает — удаляем из множества,
                            # чтобы в следующий раз можно было отправить
                            sent_users.discard(user_id)

        except Exception as e:
            logging.error(f"Ошибка при работе с базой данных в планировщике: {e}")

        await asyncio.sleep(60)

# Для совместимости алиас
schedule_daily_surprise = start_scheduler
