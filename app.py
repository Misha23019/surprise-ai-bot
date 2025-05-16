import os
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from modules.router import start, time_handler, button_handler, language_selection_handler
from modules.scheduler import start_scheduler

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")

def main():
    # Створюємо application з вбудованим job_queue
    application = Application.builder().token(TOKEN).build()

    # Обробники
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, time_handler))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Regex(r'^🌐'), language_selection_handler))

    # Запускаємо планувальник
    start_scheduler(application.job_queue)

    # Запускаємо бота
    application.run_polling()

if __name__ == "__main__":
    main()
