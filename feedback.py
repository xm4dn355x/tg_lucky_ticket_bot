# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
#                                                                      #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message
from loguru import logger


class Feedback(StatesGroup):
    """Конечный автомат формы обратной связи"""
    waiting_for_phone = State()
    waiting_for_ticket = State()
    waiting_for_text = State()

cancel = InlineKeyboardButton('Отмена', callback_data='/cancel')

cancel_kb = InlineKeyboardMarkup(row_width=1).add(cancel)
