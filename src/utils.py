from threading import Timer
from src.saver import Saver
from datetime import datetime


saver = Saver()
format ='%Y-%m-%d %H:%M:%S'


def update_info():
    pass


def send_alarm():
    date = saver.get_info_file()[0]
    if len(date) > 0:
        return [f'У домена {i} осталось {(datetime.strptime(k, format) - datetime.now()).days} дней!' \
                for i, k in date.items() if (datetime.strptime(k, format) - datetime.now()).days < 14]


