import telebot
import django
import os
from django.core.management.base import BaseCommand
from program_web.models import Feedback
from django.conf import settings


TELEGRAM_BOT_API_KEY = os.getenv('TOKENTG')
bot = telebot.TeleBot(str(settings.TELEGRAM_BOT_API_KEY), threaded=False)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sommelier_Online_Project.settings')
django.setup()


class UserState:
    WELCOME = 0
    FEEDBACK = 1
    PROJECTS = 2
    ONLINE_SOMMILIE = 3
    FEEDBACK_TEXT = 4
    FEEDBACK_ANON = 5


user_feedback_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    feedback_button = telebot.types.KeyboardButton('Залишити відгук')
    projects_button = telebot.types.KeyboardButton('Проекти')
    markup.add(feedback_button, projects_button)
    bot.send_message(message.chat.id, "Вітаю!\nЯ телеграм бот, проекту 'Онлайн Сомельє'\nБудь-ласка оберіть функцію.", reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.WELCOME)


@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    state = bot.get_state(message.from_user.id)

    if state == UserState.WELCOME:
        if message.text == 'Залишити відгук':
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            back_button = telebot.types.KeyboardButton('Назад')
            markup.add(back_button)
            bot.send_message(message.chat.id, "Будь ласка, залиште ваш відгук.", reply_markup=markup)
            bot.set_state(message.from_user.id, UserState.FEEDBACK_TEXT)

        elif message.text == 'Проекти':
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            project_online_sommilie_button = telebot.types.KeyboardButton('Онлайн Сомельє')
            back_button = telebot.types.KeyboardButton('Назад')
            markup.add(project_online_sommilie_button, back_button)
            bot.send_message(message.chat.id, "Проекти", reply_markup=markup)
            bot.set_state(message.from_user.id, UserState.PROJECTS)

    elif state == UserState.FEEDBACK_TEXT:
        if message.text == 'Назад':
            send_welcome(message)
        else:
            user_feedback_data[message.chat.id] = {'feedback': message.text}
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            anon_button = telebot.types.KeyboardButton('Залишити анонімно')
            tg_name_button = telebot.types.KeyboardButton('Залишити з ім\'ям Telegram')
            back_button = telebot.types.KeyboardButton('Назад')
            markup.add(anon_button, tg_name_button, back_button)
            bot.send_message(message.chat.id, "Ви бажаєте залишити відгук анонімно чи з вашим ім'ям Telegram?", reply_markup=markup)
            bot.set_state(message.from_user.id, UserState.FEEDBACK_ANON)

    elif state == UserState.FEEDBACK_ANON:
        if message.text == 'Назад':
            send_welcome(message)
        elif message.text == 'Залишити анонімно':
            user_feedback_data[message.chat.id]['name'] = 'anonim'
            save_feedback(message.chat.id)
            bot.send_message(message.chat.id, "Дякуємо за ваш відгук!")
            send_welcome(message)
        elif message.text == 'Залишити з ім\'ям Telegram':
            user_feedback_data[message.chat.id]['name'] = message.from_user.first_name or 'anonim'
            save_feedback(message.chat.id)
            bot.send_message(message.chat.id, "Дякуємо за ваш відгук!")
            send_welcome(message)

    elif state == UserState.PROJECTS:
        if message.text == 'Онлайн Сомельє':
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            git_hub_button = telebot.types.KeyboardButton('GitHub проекта')
            site_button = telebot.types.KeyboardButton('Посилання на проект')
            project_info_button = telebot.types.KeyboardButton('Про проект')
            back_button = telebot.types.KeyboardButton('Назад')
            markup.add(git_hub_button, site_button, project_info_button, back_button)
            bot.send_message(message.chat.id, "Онлайн Сомельє", reply_markup=markup)
            bot.set_state(message.from_user.id, UserState.ONLINE_SOMMILIE)
        elif message.text == 'Назад':
            send_welcome(message)

    elif state == UserState.ONLINE_SOMMILIE:
        if message.text == 'GitHub проекта':
            bot.send_message(message.chat.id, "https://github.com/Bevziuk2005/Sommelier_Online.git")
        elif message.text == 'Посилання на проект':
            bot.send_message(message.chat.id, "https://sommelier-online.onrender.com")
        elif message.text == 'Про проект':
            bot.send_message(message.chat.id, "Сайт пропонує користувачам можливість отримати професійні рекомендації щодо вибору вин та їх поєднання з їжею. На сайті є:\n\n- база даних з найпопулярніших вин світу;\n- зручний інтерфейс;\n- реєстрація для зручного збереження обраних вин;\n- історична довідка про виготовлення та особливості вин;\n- пошук, який дозволяє швидко отримати інформацію про будь-яке вино;\n\nСайт орієнтований як на новачків, так і на досвідчених поціновувачів вина, надаючи зручний інтерфейс та корисні інструменти для вибору ідеального вина для будь-якої нагоди.")
        elif message.text == 'Назад':
            markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            project_online_sommilie_button = telebot.types.KeyboardButton('Онлайн Сомільє')
            back_button = telebot.types.KeyboardButton('Назад')
            markup.add(project_online_sommilie_button, back_button)
            bot.send_message(message.chat.id, "Проекти", reply_markup=markup)
            bot.set_state(message.from_user.id, UserState.PROJECTS)

    else:
        bot.send_message(message.chat.id, "Будь-ласка, оберіть одну з кнопок.")


def save_feedback(chat_id):
    data = user_feedback_data.get(chat_id)
    if data:
        Feedback.objects.create(name=data['name'], feedback=data['feedback'])
        del user_feedback_data[chat_id]

