import os
from pytz import UTC
from telegram.ext import (
    ApplicationBuilder,  # <-- додати це
    Application,         # <-- залишити
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    JobQueue,
    filters,
)

from modules.router import start, time_handler, button_handler, language_selection_handler
from modules.scheduler import start_scheduler

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")

from modules.database import init_db

def main():
    init_db()
    
def main():
    application = Application.builder().token(TOKEN).build()

    # Обробники
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, time_handler))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Regex(r'^🌐'), language_selection_handler))

    # Стартуємо планувальник
    start_scheduler(application.job_queue)

    application.run_polling()


if __name__ == "__main__":
    main()
