import os
from src.saver import Saver
from datetime import datetime
import telebot
from telebot import types
from whois import whois
from whois_search import WhoisSearch
import ujson
import time


def telegram():
    api = os.environ.get('API_TELEBOT')
    bot = telebot.TeleBot(api)
    saver = Saver()
    format = '%Y-%m-%d %H:%M:%S'
    path_file = os.path.join('..', 'src', 'chat_id.json')
    path_group = os.path.join('..', 'src', 'group.json')
    try:
        @bot.message_handler(commands=['start'])
        def save_chat_id(message: types.Message) -> None:
            """
            Сохранение id в файл
            :param message: str
            :return: None
            """
            bot.send_message(message.chat.id, """Выберите режим работы бота
/info
/admin""")
            bot.register_next_step_handler(message, adding_status)

        @bot.message_handler(commands=['info', 'admin'])
        def adding_status(message: types.Message) -> None:
            if 'info' in message.text:
                group = open(path_group, 'r', encoding='utf-8')
                json_group = set(ujson.load(group))
                group.close()
                with open(path_group, 'w', encoding='utf-8') as f:
                    if message.chat.id not in json_group:
                        bot.send_message(message.chat.id, 'Уведомления включены')
                    json_group.update({message.chat.id})
                    ujson.dump(list(json_group), f)

            elif 'admin' in message.text:
                file = open(path_file, 'r', encoding='utf-8')
                json_list = set(ujson.load(file))
                file.close()
                with open(path_file, 'w', encoding='utf-8') as f:
                    if message.chat.id not in json_list:
                        bot.send_message(message.chat.id, 'Вы стали администратором')
                    json_list.update({message.chat.id})
                    ujson.dump(list(json_list), f)
                user_interation(message)
            else:
                bot.send_message(message.chat.id, 'Неверные данные. Напишите еще раз')
                bot.register_next_step_handler(message, adding_status)



        @bot.message_handler(commands=['off'])
        def del_chat_id(message: types.Message) -> None:
            """
            Удаление id из файла
            :param message: str
            :return: None
            """
            file = open(path_file, 'r', encoding='utf-8')
            json_list = ujson.load(file)
            file.close()
            try:
                with open(path_file, 'w', encoding='utf-8') as f:
                    json_list.remove(message.chat.id)
                    ujson.dump(json_list, f)
                bot.send_message(message.chat.id, 'Уведомления отключены. Для включение наберите /start')
            except ValueError:
                with open(path_file, 'w', encoding='utf-8') as f:
                    ujson.dump(json_list, f)

        @bot.message_handler(commands=['help', 'get_info', 'add_domain', 'del_domain'])
        def user_interation(message: types.Message):
            """
            Взаимодействие с пользователем
            :param message: текст пользователя
            :return: None
            """
            file = open(path_file, 'r', encoding='utf-8')
            check = ujson.load(file)
            file.close()
            if message.chat.id in check:
                if 'add_domain' in message.text:
                    bot.send_message(message.chat.id, 'Напишите название домена')
                    bot.register_next_step_handler(message, adding_domain)

                elif 'del_domain' in message.text:
                    bot.send_message(message.chat.id, 'Напишите название домена')
                    bot.register_next_step_handler(message, del_domain)

                elif 'get_info' in message.text:
                    date = saver.get_info_file()[0]
                    # проверка на пустой список
                    if len(date) > 0:
                        # сортировка по дате
                        date = dict(sorted(date.items(), key=lambda item: item[1]))
                        # Список {название домена: время жизни домена}
                        list_join = []
                        for i, k in date.items():
                            if k == 'Информация отсутствует':
                                list_join.append(f'О домене {i} нет информации')
                            else:
                                list_join.append(f'{i}: осталось {(datetime.strptime(k, format) - datetime.now()).days} дней')
                        join = '\n'.join(list_join)

                        bot.send_message(message.chat.id, f'{join}')
                    else:
                        bot.send_message(message.chat.id, 'Список пустой')
                else:
                    bot.send_message(message.chat.id, '''Список доступных команд:
/add_domain - Добавить домен
/del_domain - Удалить домен
/get_info - Список доменов
/off - для отключения уведомлений
/start - для подключения уведомлений''')

        def adding_domain(message: types.Message) -> None:
            """
            Добавление домена в список
            :param message: название домена
            :return: None
            """
            value = whois(message.text).expiration_date
            if value is not None:
                if type(value) is list:
                    value = value[1]
                domain = {message.text.upper(): str(value)}
                saver.adding_info_file(domain)
                bot.send_message(message.chat.id, 'Добавился!')
            elif '.' in message.text:
                whois_search = WhoisSearch(message.text)
                domain = {message.text.upper(): whois_search.get_date()}
                saver.adding_info_file(domain)
                bot.send_message(message.chat.id, 'Добавился!')
            else:
                bot.send_message(message.chat.id, 'Неверный домен!')

        def del_domain(message: types.Message) -> None:
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
    except:
        print('off')
        time.sleep(0.5)
        # file = open(path_file, 'r', encoding='utf-8')
        # test_json = ujson.load(file)
        # file.close()
        # for i in test_json:
        #     bot.send_message(i, 'Меня убили, но я выжил!')
        telegram()
