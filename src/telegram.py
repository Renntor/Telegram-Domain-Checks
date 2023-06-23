from src.whois import Whois
from src.saver import Saver
import ujson
from datetime import datetime
import telebot
from telebot import types


bot = telebot.TeleBot('6116448329:AAFJfwwrr1BKKJXva-OnAIkOkfWMUHkNEIo')

saver = Saver()
@bot.message_handler(content_types='text')
def user_interation(message: types.Message):
    if message.text == 'Добавить домен':
        bot.send_message(message.chat.id, 'Напишите название домена')
        bot.register_next_step_handler(message, adding_domain)
    elif message.text == 'Удалить домен':
        bot.send_message(message.chat.id, 'Напишите название домена')
        bot.register_next_step_handler(message, del_domain)
    elif message.text == 'Список доменов':
        bot.register_next_step_handler(message, get_info_domain)


def adding_domain(message: types.Message):
    whois = Whois(message.text)
    try:
        domain = {whois.get_info_domain()['result']['domain_name']: whois.get_info_domain()['result']['expiration_date']}
        saver.adding_info_file(domain)
        bot.send_message(message.chat.id, 'Добавился!')
    except TypeError:
        bot.send_message(message.chat.id, 'Неверный домен!')


def del_domain(message: types.Message):
    if saver.del_info_file(message.text.upper()):
        bot.send_message(message.chat.id, f'Домен {message.text} удален!')
    else:
        bot.send_message(message.chat.id, f'Неверный домен!')


def get_info_domain(message: types.Message):
    pass


@bot.message_handler()
def markup_button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    added_button = types.KeyboardButton("Добавить домен")
    del_button = types.KeyboardButton("Удалить домен")
    info_button = types.KeyboardButton("Список доменов")

    markup.add(info_button)
    markup.add(added_button, del_button)

    bot.send_message(message.chat.id, 'Список доступных команд', reply_markup=markup)


#
#
# def user_input(message):
#     if message == "Добавить домен":
#         bot.send_message(message.chat.id, 'Добавляем домен')
#     elif message == 'Удалить домен':
#         bot.send_message(message.chat.id, 'Удаляем домен')
#     elif message == 'Список доменов':
#         bot.send_message(message.chat.id, 'Выводим список доменов')


bot.polling(none_stop=True)


# u = Saver()
# e = Whois('ya.ru')
# w = e.get_info_domain()
# t = {w['result']["domain_name"]: w['result']['expiration_date']}
# u.adding_info_file(t)


# i = datetime.strptime('2023-12-11 19:43:57', '%Y-%m-%d %H:%M:%S')
#
# print(i - datetime.now())

#
# @bot.message_handler()
# def info(message):
#     bot.send_message(message.chat.id, f'{saver.get_info_file()}')