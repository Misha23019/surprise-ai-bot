import os
from flask import Flask, request, abort
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from modules.router import start_command, handle_text, handle_callback_query
from modules.scheduler import start_scheduler, schedule_daily_surprises
from modules.database import reset_manual_counts
import asyncio

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in environment variables")

# Создаем Flask-приложение
app = Flask(__name__)

# Создаем Telegram Application
application = ApplicationBuilder().token(TOKEN).build()

# Регистрируем хендлеры
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CallbackQueryHandler(handle_callback_query))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

# Flask endpoint для webhook
@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.headers.get("Content-Type") == "application/json":
        try:
            update = Update.de_json(request.get_json(force=True), application.bot)
            await application.process_update(update)
        except Exception as e:
            print(f"Webhook error: {e}")
            return "ERROR", 500
        return "OK"
    else:
        abort(400)

if __name__ == "__main__":
    # Запуск планировщика
    start_scheduler()
    schedule_daily_surprises()

    # Запускаем Flask сервер (используем aiohttp loop для PTB >= 20)
    port = int(os.environ.get("PORT", 5000))
    
    # Telegram Webhook должен быть установлен отдельно! Например:
    # await application.bot.set_webhook("https://yourdomain.com/webhook")
    # или настрой через Telegram BotFather

    # Запускаем Flask вручную
    import threading

    def run_flask():
        app.run(host="0.0.0.0", port=port)

    # Запускаем Flask-сервер в отдельном потоке
    threading.Thread(target=run_flask).start()

    # Запускаем асинхронную часть PTB (если нужны фоновые задачи)
    asyncio.run(application.initialize())
