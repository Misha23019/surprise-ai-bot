from flask import Flask, request
import os
from dotenv import load_dotenv
from modules.router import handle_update
from modules.scheduler import start_scheduler

load_dotenv()

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route("/")
def index():
    return "Surprise Me! бот працює ✅"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = request.get_json()
        handle_update(update)
        return "ok", 200

if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
