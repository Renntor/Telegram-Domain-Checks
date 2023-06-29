from utils import update_info, send_alarm
from telegram import telegram
from threading import Thread


if __name__ == '__main__':
    tel = Thread(target=telegram)
    info = Thread(target=update_info)
    alarm = Thread(target=send_alarm)

    tel.start()
    info.start()
    alarm.start()
    tel.join()
    info.join()
    alarm.join()


