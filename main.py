# -*- coding: utf-8 -*-
########################################################################
#                                                                      #
# Telegram-бот для проверки статуса победителей в викторине            #
# "Уютный Ямал". Основной скрипт.                                      #
#                                                                      #
# MIT License                                                          #
# Copyright (c) 2021 Michael Nikitenko                                 #
#                                                                      #
########################################################################


import os
from datetime import datetime
from sys import platform

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from loguru import logger

from feedback import Feedback
from services import get_day_period, match_winner_number, greet_kb, find_closest_place

# Init loggers
logger.add('logs/debug.log', format="{time} {level} {message}", level='DEBUG', rotation='500 MB')
logger.add('logs/info.log', format="{time} {level} {message}", level='INFO', rotation='500 MB')
logger.add('logs/errors.log', format="{time} {level} {message}", level='ERROR', rotation='500 MB')

# Init global configs
if platform == 'win32':     # Windows environment variables is peace of sh... use just an configs file
    from bot_configs import TOKEN
else:                       # If linux, or Docker, or MacOS you can use environmental variables
    TOKEN = os.environ.get('token')

# Init aiogram bot
bot = Bot(TOKEN)
dp = Dispatcher(bot)


@logger.catch
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: Message):
    """Обработчик команд /start и /help"""
    await message.answer(f'{get_day_period(datetime.now())} Я бот конкурса *Уютный Ямал!*\n\n'
                        f'Отправь мне номер своего билета и я тебе скажу какие призы ты можешь получить',
                        parse_mode='Markdown')


@logger.catch
@dp.message_handler(regexp=r'^\d+$')
async def check_winner_or_not(message: Message):
    prizes_message = match_winner_number(int(message.text))
    await message.answer(prizes_message)


@logger.catch
@dp.message_handler(content_types=ContentType.LOCATION)
async def geo_handler(message: Message):
    result = find_closest_place(message.location)
    await message.answer(result)


@logger.catch
@dp.message_handler(regexp=r'\D')
async def wrong_number(message: Message):
    """Если пользователь написал номер билета с ошибками"""
    await message.answer('введите пожалуйста номер билета правильно без пробелов, номер может содержать только цифры')


# @logger.catch
# async def feedback_start(message: Message):
#     """Запуск формы обратной связи"""
#     await message.answer('Начало формы обратной связи. ебани телефон')
#     await Feedback.waiting_for_phone.set()
#
#
# @logger.catch
# async def feedback_phone_set(message: Message, state: FSMContext):
#     """Пользователь ввёл номер телефона"""
#     try:
#         phone = message.text.strip().replace('+', '')
#     except ValueError:
#         await message.answer('Ты долбоёб, чи шо? Нормально номер введи.')
#         return
#     await state.update_data(phone=phone)
#     await message.answer('Теперь нужен номер билета')
# TODO: Переписать фидбэк на пересылание сообщения в чат


if __name__ == '__main__':
    logger.info('Bot started')
    executor.start_polling(dp, skip_updates=True)

# TODO: Обработчик для обратной связи на FSM Контактные данные, номер билета, текст обращения