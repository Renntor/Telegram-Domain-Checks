import time
import os
import ujson
from whois import whois
from src.saver import Saver
from datetime import datetime
from whois_search import WhoisSearch
from threading import Timer
import telebot

saver = Saver()
format ='%Y-%m-%d %H:%M:%S'
path_file = os.path.join('..', 'src', 'chat_id.json')
api = os.environ.get('API_TELEBOT')
bot = telebot.TeleBot(api)


def update_info() -> None:
    """
    Обновляет информацию о доменах раз в день
    :return: None
    """
    date = saver.get_info_file()[0]
    if len(date) > 0:
        # перебор из файла доменов
        for i in date.keys():
            time.sleep(0.5)
            try:
                value = whois(i).expiration_date
                if value is not None:
                    if type(value) is list:
                        value = value[1]
                    domain = {i.upper(): str(value)}
                    saver.adding_info_file(domain)
                else:
                    whois_search = WhoisSearch(i)
                    domain = {i.upper(): whois_search.get_date()}
                    saver.adding_info_file(domain)
            except Exception:
                pass
    Timer(86400, update_info).start()


def send_alarm() -> None:
    """
    Раз в день посылает в чат если аренда домена меньше 14 дней
    :return: None
    """
    date = saver.get_info_file()[0]
    if len(date) > 0:
        # список доменов с истекающим сроком
        join = [f'У домена {i} осталось {(datetime.strptime(k, format) - datetime.now()).days} дней!' \
                for i, k in date.items() if (datetime.strptime(k, format) - datetime.now()).days <= 14]
        if len(join) > 0:
            file = open(path_file, 'r', encoding='utf-8')
            test_json = ujson.load(file)
            file.close()
            for i in test_json:
                bot.send_message(i, '\n'.join(join))
    Timer(86400, send_alarm).start()


