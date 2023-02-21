import argparse
import logging
import os
import textwrap as tw
import time
from datetime import datetime

import requests
from dotenv import load_dotenv
from telegram import Bot

logger = logging.getLogger(__name__)


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
        👀 Посмотрите код-ревью преподавателя: %s.
        🕦 %s
        """ % (review['lesson_title'], review['lesson_url'], review_date)
    return tw.dedent(message)


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    load_dotenv()
    dvmn_token = os.environ.get('DEVMAN_TOKEN')
    tg_token = os.environ.get('TG_TOKEN')
    chat_id = os.environ.get('CHAT_ID')

    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    payload = {'timestamp': ''}

    bot = Bot(token=tg_token)

    parser = argparse.ArgumentParser(
        description='Получение уведомлений с сайта dvmn.org'
    )
    parser.add_argument('chat_id', nargs='?',
                        type=int, default=int(chat_id),
                        help='Ввести chat_id')
    args = parser.parse_args()
    user_id = args.chat_id

    while True:
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

        except requests.exceptions.ConnectionError:
            logger.error("Lost HTTP connection")
            time.sleep(60)
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    main()
