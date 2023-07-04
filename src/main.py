from utils import update_info, send_alarm
from telegram import telegram
from threading import Thread
import os
import ujson
import telebot


path_file = os.path.join('..', 'src', 'chat_id.json')
api = os.environ.get('API_TELEBOT')
bot = telebot.TeleBot(api)

tel = Thread(target=telegram, daemon=True)
info = Thread(target=update_info, daemon=True)
alarm = Thread(target=send_alarm, daemon=True)

try:
    if __name__ == '__main__':
        tel.start(), info.start(), alarm.start()
        tel.join(), info.join(), alarm.join()


except:
    file = open(path_file, 'r', encoding='utf-8')
    test_json = ujson.load(file)
    file.close()
    for i in test_json:
        bot.send_message(i, 'Да заткнись ты, дай хоть умереть спокойно')
