# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Вспомогательные классы и функции для проекта                         #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ContentType


def get_day_period(request: datetime):
    """Получает объект datetime и возвращает приветственное сообщение в зависимости от времени суток"""
    periods = ['Доброй ночи', 'Доброе утро!', 'Добрый день!', 'Добрый вечер!']
    return periods[request.hour // 6]  # Сутки делятся на 6 равных частей, естественно разбиваясь на периоды


def match_winner_number(number: int) -> list or bool:
    """Получает номер билета и возвращает словарь с результатами"""
    if number == 10:  # TODO: Заменить мокнутое сообщение на нормальное
        return ['Кружка', 'Худи', 'Трусы']
    elif number == 100:
        return ['Штаны']
    return False


def find_closest_place(location: ContentType.LOCATION):
    print(f"{location['latitude']}")    # TODO: Добавить координаты пунктов выдачи и поиск ближайшего
    print(f"{location['longitude']}")
    if location['latitude'] == 66.530255 and location['longitude'] == 66.625386:
        return 'ТЫ дома'
    else:
        return 'Ты не дома'


button_geo = KeyboardButton('🗺 Поделиться Геолокацией 🌐', request_location=True)
button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')
button4 = KeyboardButton('4️⃣')
button5 = KeyboardButton('5️⃣')
button6 = KeyboardButton('6️⃣')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(button_geo).add(button1).row(button2, button3, button4).insert(button5).add(button6)
