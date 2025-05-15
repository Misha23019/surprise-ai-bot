from flask import Flask, request, jsonify
from modules.router import handle_update
from modules.scheduler import start_scheduler
import os
import logging

app = Flask(__name__)

# Запускаем планировщик при старте приложения
start_scheduler()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if not update:
        return jsonify({"status": "no update"}), 400

    try:
        handle_update(update)
    except Exception as e:
        logging.exception("Ошибка обработки апдейта")
        return jsonify({"status": "error"}), 500

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=port)
