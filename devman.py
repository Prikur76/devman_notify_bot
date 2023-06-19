import argparse
import logging.config
import requests
import textwrap as tw
import time
from datetime import datetime
from telegram import Bot

import settings

logging.config.dictConfig(settings.logger_config)
logger = logging.getLogger('app_logger')


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

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {settings.DVMN_TOKEN}'}
    payload = {'timestamp': ''}

    bot = Bot(token=settings.DVMN_BOT_TOKEN)

    parser = argparse.ArgumentParser(
        description='Получение уведомлений с сайта dvmn.org'
    )
    parser.add_argument('chat_id', nargs='?',
                        type=int, default=int(settings.CHAT_ID),
                        help='Ввести chat_id')
    args = parser.parse_args()
    user_id = args.chat_id

    while True:
        logger.debug('Бот DEVMAN запущен')
        try:
            response = requests.get(
                url=long_polling_url,
                params=payload,
                headers=headers,
                timeout=25
            )
            review = response.json()
            if review['status'] == 'found':
                payload['timestamp'] = review['last_attempt_timestamp']
                code_review = review['new_attempts'][0]
                answer = get_message_for_chat(code_review)
                bot.send_message(chat_id=user_id, text=answer)
            elif review['status'] == 'timeout':
                payload['timestamp'] = datetime.timestamp(datetime.now())

        except requests.exceptions.ConnectionError as conn_err:
            logger.debug('Бот DEVMAN упал с ошибкой:')
            logger.exception(conn_err)
            time.sleep(60)
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    main()
