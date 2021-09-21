# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Вспомогательные классы и функции для проекта                         #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


from collections import namedtuple
from datetime import datetime

# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from openpyxl import load_workbook

# WINNERS_XLS = 'Призы.xlsx'
from openpyxl.worksheet.worksheet import Worksheet

WINNERS_XLS = 'Победители.xlsx'

# Winner = namedtuple('Winner', ['number', 'prizes', 'address'])
# Winner = namedtuple('Winner', ['number', 'prizes'])
# Winner = namedtuple('Winner', ['mo', 'prize', 'ticket', 'name'])
Winner = namedtuple('Winner', ['mo', 'prize', 'ticket', 'name', 'phone', 'sms'])


def get_day_period(request: datetime):
    """Получает объект datetime и возвращает приветственное сообщение в зависимости от времени суток"""
    periods = ['Доброй ночи', 'Доброе утро!', 'Добрый день!', 'Добрый вечер!']
    return periods[request.hour // 6]  # Сутки делятся на 6 равных частей, естественно разбиваясь на периоды


def get_worksheet(document_path: str) -> Worksheet:
    """Получает путь к xls файлу и возвращает активную страницу книги"""
    wb = load_workbook(document_path, read_only=True)
    return wb.active


def read_xls_winners(document_path: str) -> tuple[Winner, ...]:
    """Читает xlsx файл и возвращает его содержимое в виде кортежа из namedtuple Winner"""
    ws = get_worksheet(document_path=document_path)
    # return tuple([Winner(row[0].value, row[1].value, row[2].value)
    #               for row in ws.rows if isinstance(row[0].value, int)])
    return tuple([Winner(row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value)
                  for row_index, row in enumerate(ws.rows) if row_index != 0])


def match_winner_number(number: str) -> str:
    """Получает номер билета и возвращает словарь с результатами"""
    winners = read_xls_winners(document_path=WINNERS_XLS)
    for w in winners:
        if w.ticket == number:
            places_list = generate_pickup_places_list(w.mo)
            return f'{w.sms}\n\n{places_list}'
    return 'К сожалению не видим вашего бланка среди списка победителей.\n' \
           'Если ошиблись, или хотите проверить другой бланк, просто отправьте мне его номер.\n\n' \
           'Если у Вас возникли какие-то дополнительные вопросы - обращайтесь к нам по электронной почте uyamal@bk.ru'


# def find_closest_place(location: ContentType.LOCATION):
#     print(f"{location['latitude']}")
#     print(f"{location['longitude']}")
#     if location['latitude'] == 66.530255 and location['longitude'] == 66.625386:
#         return 'ТЫ дома'
#     else:
#         return 'Ты не дома'


# # Города окружного значения
# shd = KeyboardButton('Салехард')
# gub = KeyboardButton('Губкинский')
# # gub = KeyboardButton(shd) # Для тестирования отловаливания багов
# lbt = KeyboardButton('Лабытнанги')
# mur = KeyboardButton('Муравленко')
# nur = KeyboardButton('Новый Уренгой')
# noy = KeyboardButton('Ноябрьск')
# # Районы
# krasn = KeyboardButton('Красноселькупский район')
# nadym = KeyboardButton('Надымский и Надымский район')
# priural = KeyboardButton('Приуральский район')
# pur = KeyboardButton('Пуровский район')
# taz = KeyboardButton('Тазовский район')
# shur = KeyboardButton('Шурышкарский район')
# yamalsky = KeyboardButton('Ямальский район')
#
#
# greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# # greet_kb.add(button_geo).add(button1).row(button2, button3, button4).insert(button5).add(button6)
# greet_kb.row(shd, gub, lbt).row(mur, nur, noy).row(krasn, priural).row(nadym).row(pur, taz).row(shur, yamalsky)


# MO = namedtuple('MO', ['shd', 'lbt', 'yamalsky', 'priuralsky', 'shur', 'nadymsky', 'nur',
#                        'taz', 'pur', 'krasn', 'gub', 'mur', 'noy'])
Place = namedtuple('Place', ['mo', 'city', 'name', 'address', 'working_time', 'phone'])


def read_xls_places(document_path: str) -> tuple:
    """Читает xls файл со списком пунктов выдачи и возвращает структуру данных с инфой о пунктах выдачи"""
    ws = get_worksheet(document_path=document_path)
    return tuple([Place(row[0].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value)
                  for i, row in enumerate(ws.rows) if i != 0])


def get_pickup_places_list(mo: str) -> tuple:
    """Получает название МО и возвращает список пунктов выдачи в виде кортежа"""
    return tuple([i for i in read_xls_places('Пункты выдачи.xlsx') if i.mo == mo])


def generate_pickup_places_list(mo: str) -> str:
    """Получает название МО и возвращает текст с пунктами выдачи"""
    places_list = get_pickup_places_list(mo)
    if len(places_list) == 1:
        address_plural_or_not = 'по адресу:'
    else:
        address_plural_or_not = 'по одному из адресов:'
    res = f'Вы можете забрать подарок по {address_plural_or_not}\n'
    for place in places_list:
        res += f"- *{place.city}* {place.address} Время работы: {place.working_time} Тел.: {place.phone}\n"
    res += '\n' \
           'Если у Вас возникли какие-то дополнительные вопросы - обращайтесь к нам по электронной почте uyamal@bk.ru'
    return res


# def generate_pickup_points_kb(places: tuple, mo=None) -> ReplyKeyboardMarkup:
#     """Генерирует клавиатуру с пунктами выдачи"""
#     # kb = ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder='Залупа', resize_keyboard=True)
#     # if mo:
#     #     for place in places:
#     #         if place.mo == mo:
#     #             print(place)
#     #             kb.add(KeyboardButton(f'{place.name}', callback_data='1488'))
#     # else:
#     #     for place in places:
#     #         print(place)
#     #         kb.add(KeyboardButton(f'{place.name}', callback_data='1488'))
#     #     kb.add(KeyboardButton('Назад', callback_data='Отмена'))
#     # return kb
#     kb = InlineKeyboardMarkup()
#     if mo:
#         for place in places:
#             if place.mo == mo:
#                 print(place)
#                 kb.add(InlineKeyboardButton(f'{place.name}', callback_data='btn1'))
#     else:
#         for place in places:
#             print(place)
#             kb.add(InlineKeyboardButton(f'{place.name}', callback_data='btn1'))
#         kb.add(InlineKeyboardButton('Назад', callback_data='Отмена'))
#     return kb


if __name__ == '__main__':
    # data = read_xls_places('Пункты выдачи.xlsx')
    # for d in data:
    #     print(d)
    # keyboard = generate_pickup_points_kb(data)
    # print('!!!!!!!!!!!!')
    # keyboard = generate_pickup_points_kb(data, 'Лабытнанги')
    data = read_xls_winners('Noyabrsk (1).xlsx')
    for d in data:
        print(d)
        places = get_pickup_places_list(d.mo)
        for place in places:
            print(f"\t{place}")
    print(match_winner_number(number='005544'))
    print(match_winner_number(number='017447'))
    print(match_winner_number(number='001488'))
