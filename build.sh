#!/bin/bash

# Запуск gunicorn у фоновому режимі
python -m gunicorn Sommelier_Online_Project.asgi:application -k uvicorn.workers.UvicornWorker &

# Запуск телеграм-бота
python manage.py program_tg
