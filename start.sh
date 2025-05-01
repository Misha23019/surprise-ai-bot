#!/bin/bash

# Активуємо правильний python, якщо потрібно
if command -v python3 &>/dev/null; then
  exec python3 app.py
else
  exec python app.py
fi
