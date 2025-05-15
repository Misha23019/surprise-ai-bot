#!/bin/bash

# Активируем виртуальное окружение, если нужно
# source venv/bin/activate

export FLASK_APP=app.py
export FLASK_ENV=production

# Запускаем Flask с привязкой ко всем интерфейсам и порт из окружения
flask run --host=0.0.0.0 --port=${PORT:-5000}
