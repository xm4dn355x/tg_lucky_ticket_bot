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
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType
from loguru import logger

from feedback import Feedback, cancel_kb
from services import get_day_period, match_winner_number, find_closest_place

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
dp = Dispatcher(bot, storage=MemoryStorage())


@logger.catch
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: Message):
    """Обработчик команд /start и /help"""
    await message.answer(f'{get_day_period(datetime.now())} Я бот конкурса *Уютный Ямал!*\n\n'
                        f'Отправь мне номер своего билета и я тебе скажу какие призы ты можешь получить',
                        parse_mode='Markdown')


@logger.catch
@dp.message_handler(commands=['feedback'])
async def feedback_start(message: Message):
    """Запуск формы обратной связи"""
    await message.answer('Вы попали в форму обратной связи. ', reply_markup=cancel_kb)
    await Feedback.waiting_for_phone.set()


@dp.message_handler(state='*', commands=['cancel', 'Отмена'])
async def cancel_handler(message: types.Message, state: FSMContext):    # FIXME: Разобраться почему это говно не работает с кнопки
    """Позволяет пользователю отменить работу с формой"""
    current_state = await state.get_state()
    if current_state is None:
        return
    logger.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Операция отменена', reply_markup=types.ReplyKeyboardRemove())


@logger.catch
@dp.message_handler(state=Feedback.waiting_for_phone)
async def feedback_phone_set(message: Message, state: FSMContext):
    """Пользователь ввёл номер телефона"""
    try:
        phone = int(message.text.strip().replace('+', ''))
    except ValueError:
        await message.answer('Ты долбоёб, чи шо? Нормально номер введи.')
        return
    await state.update_data(phone=phone)
    await Feedback.next()
    await message.answer('Теперь нужен номер билета')


@logger.catch
@dp.message_handler(state=Feedback.waiting_for_ticket)
async def feedback_ticket_set(message: Message, state: FSMContext):
    """Пользователь ввёл номер билета"""
    try:
        ticket = message.text.strip()
    except ValueError:
        await message.answer('Ты долбоёб, чи шо? Нормально номер билета введи.')
        return
    await state.update_data(ticket=ticket)
    await Feedback.next()
    await message.answer('Теперь текст обращения')


@logger.catch
@dp.message_handler(state=Feedback.waiting_for_text)
async def feedback_text_set(message: Message, state: FSMContext):
    """Пользователь ввёл текст вопроса"""
    text = message.text.strip()
    await state.update_data(text=text)
    user_data = await state.get_data()
    await message.answer(f"Ваше обращение:\n\nТелефон: {user_data['phone']}\nНомер билета: {user_data['ticket']}\n"
                         f"Текст обращения: {user_data['text']}\n\n"
                         f"Спасибо за обращение! "
                         f"В скором времени с Вами свяжутся по указанному в заявке номеру телефона")
    await state.finish()


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


if __name__ == '__main__':
    logger.info('Bot started')
    executor.start_polling(dp, skip_updates=True)

# TODO: Обработчик для обратной связи, добавить отправку на email