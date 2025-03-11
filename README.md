# Sommelier Online

## Опис проєкту
Sommelier Online - це веб-додаток, створений для підбору вин відповідно до смакових уподобань користувачів. Проєкт допомагає як професійним сомельє, так і любителям знаходити ідеальні поєднання вин та страв.

## Використані технології
- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS
- **База даних**: PostgreSQL
- 
## Відео-презентація
Детальніше про проєкт можна дізнатися у відео-презентації:

[![Переглянути на YouTube](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://youtu.be/CVPuStB3EuU)

## Запуск проєкту
### Локальний запуск
1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/Bevziuk2005/Sommelier_Online.git
   ```
2. Перейдіть у каталог проєкту:
   ```bash
   cd Sommelier_Online
   ```
3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
4. Виконайте міграції:
   ```bash
   python manage.py migrate
   ```
5. Запустіть сервер:
   ```bash
   python manage.py runserver
   ```
6. Перейдіть у браузері за адресою `http://127.0.0.1:8000/`.

### Запуск через Docker
1. Побудуйте Docker-образ:
   ```bash
   docker build -t sommelier_online .
   ```
2. Запустіть контейнер:
   ```bash
   docker run -p 8000:8000 sommelier_online
   ```
3. Додаток буде доступний за адресою `http://localhost:8000/`.



## Контакти
Якщо у вас є питання або пропозиції, зв'яжіться зі мною через GitHub Issues або електронну пошту.

