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
from aiogram.types import Message, ContentType
from loguru import logger

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
    prizes = match_winner_number(int(message.text))
    if prizes:
        answer = ' '.join(prizes)   # TODO: Заменить мокнутое сообщение на нормальное
        await message.answer(answer, reply_markup=greet_kb)
    else:
        await message.answer('К сожалению Вы ничего не выиграли...')


@logger.catch
@dp.message_handler(content_types=ContentType.LOCATION)
async def geo_handler(message: Message):
    result = find_closest_place(message.location)
    await message.answer(result)


if __name__ == '__main__':
    logger.info('Bot started')
    executor.start_polling(dp, skip_updates=True)
