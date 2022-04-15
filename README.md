### Homework Bot

```
Телеграм-бот для отслеживания статуса проверки проектной работы на Яндекс.Практикум.
Присылает сообщения, когда статус изменен - взято в проверку, есть замечания, зачтено.
```

### Технологии:
- Python 3.9
- python-dotenv 0.19.0
- python-telegram-bot 13.7

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/m00nrock/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```


Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Записать в переменные окружения (файл .env) необходимые ключи:
- PRACTICUM_TOKEN: токен профиля на Яндекс.Практикуме
- TELEGRAM_TOKEN: токен телеграм-бота
- TELEGRAM_CHAT_ID: свой ID в телеграме

Запустить бот:

```
python3 homework.py
```
