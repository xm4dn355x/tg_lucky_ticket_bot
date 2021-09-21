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

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked
from loguru import logger

from services import get_day_period, match_winner_number

# Init loggers
logger.add('logs/debug.log', format="{time} {level} {message}", level='DEBUG', rotation='500 MB')
logger.add('logs/info.log', format="{time} {level} {message}", level='INFO', rotation='500 MB')
logger.add('logs/errors.log', format="{time} {level} {message}", level='ERROR', rotation='500 MB')

# Init global configs
if platform == 'win32':  # Windows environment variables is peace of sh... use just an configs file
    from bot_configs import TOKEN
else:  # If linux, or Docker, or MacOS you can use environmental variables
    TOKEN = os.environ.get('token')

# Init aiogram bot
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@logger.catch
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: Message):
    """Обработчик команд /start и /help"""
    await message.answer(f'{get_day_period(datetime.now())} Я бот викторины *Уютный Ямал!*\n\n'
                         f'Отправьте мне номер своего бланка и я проверю нет ли у меня подарка для Вас',
                         parse_mode='Markdown')


@logger.catch
@dp.message_handler(regexp=r'^\d+$')
async def check_winner_or_not(message: Message):
    prizes_message = match_winner_number(message.text)
    try:
        await message.answer(prizes_message, parse_mode='Markdown')
    except BotBlocked as err:
        print(f'Bot Blocked: {err.message} {message.from_user}')
        logger.error(f'Bot Blocked: {err.message} {message.from_user}')


@logger.catch
@dp.message_handler(regexp=r'\D')
async def wrong_number(message: Message):
    """Если пользователь написал номер билета с ошибками"""
    try:
        await message.answer(
            'Введите пожалуйста номер бланка правильно без пробелов, номер может содержать только цифры\n\n'
            'Если у Вас возникли какие-то дополнительные вопросы - обращайтесь к нам по электронной почте: uyamal@bk.ru')
    except BotBlocked as err:
        print(f'Bot Blocked: {err.message} {message.from_user}')
        logger.error(f'Bot Blocked: {err.message} {message.from_user}')


if __name__ == '__main__':
    logger.info('Bot started')
    executor.start_polling(dp, skip_updates=True)
