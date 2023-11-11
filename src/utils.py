import time
import os
from src.saver import Saver
from datetime import datetime
import ujson
from whois_search import WhoisSearch
from threading import Timer
import telebot

saver = Saver()
format ='%Y-%m-%d %H:%M:%S'
info_file = os.path.join('..', 'src', 'info.json')
api = os.environ.get('API_TELEBOT')
bot = telebot.TeleBot(api)


def update_info() -> None:
    """
    Обновляет информацию о доменах раз в день
    :return: None
    """
    try:
        date = saver.get_info_file()[0]
        if len(date) > 0:
            # перебор из файла доменов
            for i in date.keys():
                time.sleep(0.5)
                try:
                    # обновление данных по домену
                    whois_search = WhoisSearch(i)
                    domain = {i.upper(): whois_search.get_date()}
                    saver.adding_info_file(domain)
                except BaseException:
                    pass
        Timer(86400, update_info).start()
    except BaseException:
        time.sleep(30)
        update_info()


def send_alarm() -> None:
    """
    Раз в день посылает в чат если аренда домена меньше 14 дней
    :return: None
    """
    try:
        date = saver.get_info_file()[0]
        if len(date) > 0:
            date = dict(sorted(date.items(), key=lambda item: item[1]))
            # список доменов с истекающим сроком
            join = []
            for i, k in date.items():
                if k == 'Информация отсутствует':
                    continue
                elif (datetime.strptime(k, format) - datetime.now()).days <= 14:
                    join.append(f'У домена {i} осталось {(datetime.strptime(k, format) - datetime.now()).days} дней!')
            # отправка доменов с истекающим сроком жизни
            if len(join) > 0:
                file = open(info_file, 'r', encoding='utf-8')
                test_json = ujson.load(file)
                file.close()
                for i in test_json:
                    bot.send_message(i, '\n'.join(join))
        Timer(86400, send_alarm).start()
    except BaseException:
        time.sleep(10)
        send_alarm()
