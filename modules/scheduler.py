from apscheduler.schedulers.background import BackgroundScheduler
from modules.limits import reset_limits
import logging

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_limits, "cron", hour=0, minute=0)  # каждый день в 00:00 UTC
    scheduler.start()
    logging.info("✅ Планувальник запущено")
