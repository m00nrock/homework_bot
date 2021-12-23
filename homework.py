import logging
import os
import sys
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN', default='SUP3R-S3CR3T-K3Y-F0R-MY-PR0J3CT')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', default='SUP3R-S3CR3T')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', default='123456')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
BOT = telegram.Bot(token=TELEGRAM_TOKEN)


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.debug('Бот успешно запущен.')


class MyException(Exception):
    """Кастомное исключение для бота."""

    pass


def send_message(bot, message):
    """Отправить сообщение в телеграм."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info(f'Бот отправил сообщение. {message}')
    except MyException:
        logging.error('Бот не отправил сообщение.')
        return 'Не удалось отправить сообщение.'


def get_api_answer(current_timestamp):
    """Получить ответ от сервера практикума по API."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    homework_statuses = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if homework_statuses.status_code != 200:
        logging.error(
            f'Сбой работы. Ответ сервера {homework_statuses.status_code}')
        send_message(
            BOT, f'Сбой работы. Ответ сервера {homework_statuses.status_code}')
        raise MyException(
            f'Сбой работы. Ответ сервера {homework_statuses.status_code}')
    status_json = homework_statuses.json()
    return status_json


def check_response(response):
    """Проверить правильность ответа от сервера."""
    if not isinstance(response['homeworks'], list):
        logging.error('Запрос к серверу пришёл не в виде списка')
        send_message(BOT, 'Запрос к серверу пришёл не в виде списка')
        raise MyException('Некорректный ответ сервера')
    return response['homeworks']


def parse_status(homework):
    """Проверить статус работы в ответе сервера."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status not in HOMEWORK_STATUSES:
        logging.error('Статус не обнаружен в списке')
        send_message(BOT, 'Статус не обнаружен в списке')
        raise MyException('Статус не обнаружен в списке')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверить обязательные для работы бота переменные."""
    if (PRACTICUM_TOKEN is None
       or TELEGRAM_CHAT_ID is None
       or TELEGRAM_TOKEN is None):
        return False
    return True


def main():
    """Основная логика работы бота."""
    if check_tokens() is False:
        logging.critical('Всё плохо, зовите админа')
        return 0
    current_timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            logging.info(f'Получили список работ {homework}')
            if len(homework) > 0:
                send_message(BOT, parse_status(homework[0]))
            logging.info('Заданий нет')
            current_timestamp = response['current_date']
            time.sleep(RETRY_TIME)

        except KeyboardInterrupt:
            stop = input('Прервать работу бота? (Y)')
            if stop == 'Y':
                break
            elif stop != 'Y':
                print('Бот работает дальше')

        except Exception as error:
            logging.error(f'Сбой в работе программы: {error}')
            send_message(BOT, f'Сбой в работе программы: {error}')
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
