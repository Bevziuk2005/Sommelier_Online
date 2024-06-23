#!/bin/bash

python -m gunicorn Sommelier_Online_Project.asgi:application -k uvicorn.workers.UvicornWorker &

python manage.py program_tg
