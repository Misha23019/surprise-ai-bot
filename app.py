import os
import pytz
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    JobQueue,
    filters,
)
from modules.router import start, time_handler, button_handler, language_selection_handler
from modules.scheduler import start_scheduler

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")

def main():
    # Явно вказуємо timezone через pytz — це ключ до вирішення
    job_queue = JobQueue(timezone=pytz.UTC)
    job_queue.start()

    application = Application.builder().token(TOKEN).job_queue(job_queue).build()

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


    # Устанавливаем вебхук вручную (можно через Telegram API)
    # await application.bot.set_webhook("https://yourserver.com/webhook")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
