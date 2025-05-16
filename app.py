import os
import logging
from modules.telegram import create_application

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in environment variables")

def main():
    application = create_application(TOKEN)
    logging.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
