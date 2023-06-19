import logging
import os

from telegram import Bot
from dotenv import load_dotenv

load_dotenv()


DVMN_TOKEN = os.environ.get('DEVMAN_TOKEN')
DVMN_BOT_TOKEN = os.environ.get('DEVMAN_BOT_TOKEN')
HELP_BOT_TOKEN = os.environ.get('HELP_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


class HelpHandler(logging.Handler):

    def emit(self, record):
        message = self.format(record)
        bot = Bot(token=HELP_BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        },
        'simple_format': {
            'format': '{message}',
            'style': '{'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format'
        },
        'bot': {
            '()': HelpHandler,
            'level': 'DEBUG',
            'formatter': 'simple_format',
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['console', 'bot']
        }
    },
}