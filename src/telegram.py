import os
from src.saver import Saver
from datetime import datetime
import telebot
from telebot import types
from whois_search import WhoisSearch
import ujson
import time


def telegram():
    api = os.environ.get('API_TELEBOT')
    bot = telebot.TeleBot(api)
    saver = Saver()
    format = '%Y-%m-%d %H:%M:%S'
    chat_id_file = os.path.join('..', 'src', 'chat_id.json')
    info_file = os.path.join('..', 'src', 'info.json')
    try:
        @bot.message_handler(commands=['start'])
        def save_chat_id(message: types.Message) -> None:
            """
            Сохранение id в файл
            :param message: str
            :return: None
            """
            bot.send_message(message.chat.id, "Выберите режим работы бота\n/info\n/admin")
            bot.register_next_step_handler(message, adding_status)

        @bot.message_handler(commands=['info', 'admin'])
        def adding_status(message: types.Message) -> None:
            """
            Добавление статус чата в файл
            :param message: str
            :return: None
            """
            if message.text in ['/info', '/info@'+f'{bot.get_me().username}']:
                group = open(info_file, 'r', encoding='utf-8')
                json_group = set(ujson.load(group))
                group.close()
                with open(info_file, 'w', encoding='utf-8') as f:
                    if message.chat.id not in json_group:
                        bot.send_message(message.chat.id, 'Уведомления включены')
                    else:
                        bot.send_message(message.chat.id, 'Уведомления уже включены')
                    json_group.update({message.chat.id})
                    ujson.dump(list(json_group), f)

            elif message.text in ['/admin', '/admin@'+f'{bot.get_me().username}']:
                file = open(chat_id_file, 'r', encoding='utf-8')
                json_list = set(ujson.load(file))
                file.close()
                with open(chat_id_file, 'w', encoding='utf-8') as f:
                    if message.chat.id not in json_list:
                        bot.send_message(message.chat.id, 'Вы стали администратором')
                    else:
                        bot.send_message(message.chat.id, 'Вы уже являетесь администратором')
                    json_list.update({message.chat.id})
                    ujson.dump(list(json_list), f)
                user_interation(message)

        @bot.message_handler(commands=['off'])
        def del_chat_id(message: types.Message):
            """
            Информация об удалении роли
            :param message: str
            :return: None
            """
            bot.send_message(message.chat.id, "Выберите режим работы бот\n/off_info\n/off_admin")

        @bot.message_handler(commands=['off_info', 'off_admin'])
        def del_id(message: types.Message) -> None:
            """
            Удаление id из файла
            :param message: str
            :return: None
            """
            #  удаление из админки
            if message.text in ['/off_admin', '/off_admin@'+f'{bot.get_me().username}']:
                file = open(chat_id_file, 'r', encoding='utf-8')
                json_list = ujson.load(file)
                file.close()
                try:
                    with open(chat_id_file, 'w', encoding='utf-8') as f:
                        json_list.remove(message.chat.id)
                        ujson.dump(json_list, f)
                    bot.send_message(message.chat.id, 'Админка отключена. Для выбора роли наберите /start')
                except ValueError:
                    with open(chat_id_file, 'w', encoding='utf-8') as f:
                        ujson.dump(json_list, f)
                    bot.send_message(message.chat.id, 'Вы не являетесь админом')

            #  удаление из информации
            elif message.text in ['/off_info', '/off_info@'+f'{bot.get_me().username}']:
                file_group = open(info_file, 'r', encoding='utf-8')
                json_group = ujson.load(file_group)
                file_group.close()
                try:
                    with open(info_file, 'w', encoding='utf-8') as f:
                        json_group.remove(message.chat.id)
                        ujson.dump(json_group, f)
                    bot.send_message(message.chat.id, 'Уведомления отключены. Для выбора роли наберите /start')
                except ValueError:
                    with open(info_file, 'w', encoding='utf-8') as f:
                        ujson.dump(json_group, f)
                    bot.send_message(message.chat.id, 'Вы не подписаны на получение информации')

        @bot.message_handler(commands=['help', 'get_info', 'add_domain', 'del_domain'])
        def user_interation(message: types.Message):
            """
            Взаимодействие с пользователем
            :param message: текст пользователя
            :return: None
            """
            file = open(chat_id_file, 'r', encoding='utf-8')
            check = ujson.load(file)
            file.close()
            if message.chat.id in check:
                if message.text in ['/add_domain', 'add_domain@'+f'{bot.get_me().username}']:
                    bot.send_message(message.chat.id, 'Напишите название домена')
                    bot.register_next_step_handler(message, adding_domain)

                elif message.text in ['/del_domain', '/del_domain@'+f'{bot.get_me().username}']:
                    bot.send_message(message.chat.id, 'Напишите название домена')
                    bot.register_next_step_handler(message, del_domain)

                elif message.text in ['/get_info', '/get_info@'+f'{bot.get_me().username}']:
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
                                list_join.append(f'{i}: осталось {(datetime.strptime(k, format) - datetime.now()).days}\
 дней')
                        join = '\n'.join(list_join)

                        bot.send_message(message.chat.id, f'{join}')
                    else:
                        bot.send_message(message.chat.id, 'Список пустой')
                elif message.text in ['/help', '/help@' + f'{bot.get_me().username}']:
                    bot.send_message(message.chat.id, '''Список доступных команд:
/add_domain - Добавить домен
/del_domain - Удалить домен
/get_info - Список доменов
/off - для отключения режима работы
/start - для выбора работы бота''')

        def adding_domain(message: types.Message) -> None:
            """
            Добавление домена в список
            :param message: название домена
            :return: None
            """
            if '.' in message.text:
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
    except BaseException:
        time.sleep(0.5)
        telegram()

