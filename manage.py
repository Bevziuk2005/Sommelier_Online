#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sommelier_Online_Project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Check if the command is to run the Telegram bot
    if len(sys.argv) > 1 and sys.argv[1] == 'program_tg':
        from program_web.management.commands.program_tg import Command as TelegramBotCommand
        bot_command = TelegramBotCommand()
        bot_command.handle()
    else:
        execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

