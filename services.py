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

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ContentType
from openpyxl import load_workbook


WINNERS_XLS = 'Призы.xlsx'

Winner = namedtuple('Winner', ['number', 'prizes', 'address'])


def get_day_period(request: datetime):
    """Получает объект datetime и возвращает приветственное сообщение в зависимости от времени суток"""
    periods = ['Доброй ночи', 'Доброе утро!', 'Добрый день!', 'Добрый вечер!']
    return periods[request.hour // 6]  # Сутки делятся на 6 равных частей, естественно разбиваясь на периоды


def read_xls(document_path: str) -> set:
    """Читает xlsx файл и возвращает его содержимое в виде кортежа из namedtuple Winner"""
    wb = load_workbook(document_path, read_only=True)
    ws = wb.active
    res = tuple([Winner(row[0].value, row[1].value, row[2].value) for row in ws.rows if isinstance(row[0].value, int)])
    return res


def match_winner_number(number: int) -> str:
    """Получает номер билета и возвращает словарь с результатами"""
    print(type(number))
    winners = read_xls(document_path=WINNERS_XLS)
    for w in winners:
        if w.number == number:
            return f'Поздравляем! Вы выиграли: {w.prizes}! Вы можете получить свои подарки по адресу: {w.address}'
    return 'К сожалению не видим вашего билета среди списка победителей.\nМожет опечатались? ' \
           'В любой момент можете отправить номер билета боту и узнать результат'# FIXME: Дополнить про обратную связь


def find_closest_place(location: ContentType.LOCATION):
    print(f"{location['latitude']}")    # TODO: Добавить координаты пунктов выдачи и поиск ближайшего
    print(f"{location['longitude']}")
    if location['latitude'] == 66.530255 and location['longitude'] == 66.625386:
        return 'ТЫ дома'
    else:
        return 'Ты не дома'


# Города окружного значения
shd = KeyboardButton('Салехард')
gub = KeyboardButton('Губкинский')
# gub = KeyboardButton(shd) # Для тестирования отловаливания багов
lbt = KeyboardButton('Лабытнанги')
mur = KeyboardButton('Муравленко')
nur = KeyboardButton('Новый Уренгой')
noy = KeyboardButton('Ноябрьск')
# Районы
krasn = KeyboardButton('Красноселькупский район')
nadym = KeyboardButton('Надымский и Надымский район')
priural = KeyboardButton('Приуральский район')
pur = KeyboardButton('Пуровский район')
taz = KeyboardButton('Тазовский район')
shur = KeyboardButton('Шурышкарский район')
yamalsky = KeyboardButton('Ямальский район')


greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# greet_kb.add(button_geo).add(button1).row(button2, button3, button4).insert(button5).add(button6)
greet_kb.row(shd, gub, lbt).row(mur, nur, noy).row(krasn, priural).row(nadym).row(pur, taz).row(shur, yamalsky)

if __name__ == '__main__':
    data = read_xls('Призы.xlsx')
    for d in data:
        print(d)