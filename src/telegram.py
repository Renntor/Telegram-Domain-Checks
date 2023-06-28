import os
from src.saver import Saver
from datetime import datetime
import telebot
from telebot import types
from whois import whois
from whois_search import WhoisSearch


api = os.environ.get('API_TELEBOT')
bot = telebot.TeleBot(api)
saver = Saver()
format = '%Y-%m-%d %H:%M:%S'


@bot.message_handler(content_types='text')
def user_interation(message: types.Message):
    """
    Взаимодействие с пользователем
    :param message: текст пользователя
    :return: None
    """

    if message.text in ['Добавить домен', '/add_domain']:
        bot.send_message(message.chat.id, 'Напишите название домена')
        bot.register_next_step_handler(message, adding_domain)
    elif message.text in ['Удалить домен', '/del_domain']:
        bot.send_message(message.chat.id, 'Напишите название домена')
        bot.register_next_step_handler(message, del_domain)
    elif message.text in ['Список доменов', '/get_info'] :
        date = saver.get_info_file()[0]
        # проверка на пустой список
        if len(date) > 0:
            # Вывод название домена: время жизни
            join = '\n'.join([f"{i}: осталось {(datetime.strptime(k, format) - datetime.now()).days}\
 дней" for i, k in date.items()])
            bot.send_message(message.chat.id, f'{join}')
        else:
            bot.send_message(message.chat.id, 'Список пустой')
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        added_button = types.KeyboardButton("Добавить домен")
        del_button = types.KeyboardButton("Удалить домен")
        info_button = types.KeyboardButton("Список доменов")

        markup.add(info_button)
        markup.add(added_button, del_button)

        bot.send_message(message.chat.id, '''Список доступных команд:
/add_domain - Добавить домен
/del_domain - Удалить домен
/get_info - Список доменов''', reply_markup=markup)


def adding_domain(message: types.Message):
    """
    Добавление домена в список
    :param message: название домена
    :return: None
    """
    try:
        value = whois(message.text).expiration_date
        if value is not None:
            if type(value) is list:
                value = value[1]
            domain = {message.text.upper(): str(value)}
            saver.adding_info_file(domain)
            bot.send_message(message.chat.id, 'Добавился!')
        else:
            whoisserch = WhoisSearch(message.text)
            domain = {message.text.upper(): whoisserch.get_date()}
            saver.adding_info_file(domain)
            bot.send_message(message.chat.id, 'Добавился!')
    except TypeError:
        bot.send_message(message.chat.id, 'Неверный домен!')


def del_domain(message: types.Message):
    """
    Удаление домена из списка
    :param message: название домена
    :return: None
    """
    if saver.del_info_file(message.text.upper()):
        bot.send_message(message.chat.id, f'Домен {message.text} удален!')
    else:
        bot.send_message(message.chat.id, f'Неверный домен!')


bot.polling(none_stop=True)
