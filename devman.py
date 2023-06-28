import argparse
import logging
import os
import requests
import textwrap as tw
import time

from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot

logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        message = self.format(record)
        self.tg_bot.send_message(
            chat_id=self.chat_id,
            text=message)


def get_message_for_chat(review):
    """Готовит информацию для публикации в tg"""
    review_date = datetime.fromisoformat(review['submitted_at'])\
        .strftime("%d.%m.%Y %H:%M")
    message = """\
    🔔🔔🔔
    😊 Ура! 🎊 Преподаватель проверил вашу работу!🎉
    📃 Урок '%s' сдан!💪
    👀 Перейти к уроку: %s.
    🕦 %s
    """ % (review['lesson_title'], review['lesson_url'], review_date)

    if review['is_negative']:
        message = """\
        🔔🔔🔔
        😞 К сожалению, урок '%s' не пройден.👎
        👀 Посмотреть код-ревью преподавателя: %s.
        🕦 %s
        """ % (review['lesson_title'], review['lesson_url'], review_date)
    return tw.dedent(message)


def main():
    load_dotenv()

    admin_chat_id = os.environ.get('CHAT_ID')
    admin_bot = Bot(token=os.environ.get('ADMIN_BOT_TOKEN'))
    admin_bot_handler = TelegramLogsHandler(
        admin_bot, admin_chat_id)
    admin_bot_handler.setLevel(logging.DEBUG)
    botformatter = logging.Formatter(
        fmt='{message}', style='{')
    admin_bot_handler.setFormatter(botformatter)
    logger.addHandler(admin_bot_handler)

    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.ERROR)
    streamformatter = logging.Formatter(
        fmt='{asctime} - {levelname} - {name} - {message}',
        style='{')
    streamhandler.setFormatter(streamformatter)
    logger.addHandler(streamhandler)

    parser = argparse.ArgumentParser(
        description='Получение уведомлений с сайта dvmn.org'
    )
    parser.add_argument('chat_id', nargs='?',
                        type=int, default=admin_chat_id,
                        help='Ввести chat_id')
    args = parser.parse_args()
    user_id = args.chat_id

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f"Token {os.environ.get('DEVMAN_TOKEN')}"}
    payload = {'timestamp': ''}
    main_bot = Bot(token=os.environ.get('DEVMAN_BOT_TOKEN'))
    logger.debug('Бот DEVMAN запущен')

    while True:
        try:
            response = requests.get(
                url=long_polling_url,
                params=payload,
                headers=headers,
                timeout=25
            )
            response.raise_for_status()

            review = response.json()
            if review['status'] == 'found':
                payload['timestamp'] = review['last_attempt_timestamp']
                code_review = review['new_attempts'][0]
                answer = get_message_for_chat(code_review)
                main_bot.send_message(chat_id=user_id, text=answer)
            elif review['status'] == 'timeout':
                payload['timestamp'] = datetime.timestamp(datetime.now())

        except requests.exceptions.HTTPError as http_err:
            logger.debug('Бот DEVMAN упал с ошибкой:')
            logger.exception(http_err)
        except requests.exceptions.ConnectionError as conn_err:
            logger.debug('Бот DEVMAN упал с ошибкой:')
            logger.exception(conn_err)
            time.sleep(60)
        except requests.exceptions.ConnectTimeout as ct_err:
            logger.debug('Бот DEVMAN упал с ошибкой:')
            logger.exception(ct_err)
            time.sleep(60)
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    main()
