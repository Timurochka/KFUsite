import sqlite3, asyncio
import config  # файл с токеном
import logging
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
import keyboards as kb
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher


logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

db = SQLighter('db.db')


# Приветствие
@dp.message_handler(commands=["start"])
async def hello(message: types.Message):
    await message.answer("Привет :)\nЯ могу помочь тебе узнать твой рейтинг в списке поступающих\nПодпишись, чтобы продолжить", reply_markup=kb.greet_kb)


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались")
    await message.answer("Введите, пожалуйста, свой снилс в формате XXXXXXXXXXX (без тире и пробелов) ")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы отписались от рассылки.")


# Обработка направлений
'''
@dp.message_handler()
async def snils_msg_handler(message: types.Message):
    mt = message.text
    if db.subscriber_exists(message.from_user.id):
'''

# Ввод снилса
@dp.message_handler()
async def snils_msg_handler(message: types.Message):
    mt = message.text
    if mt.isdigit() and len(mt) == 11:
        m = ""
        c = 0
        for t in mt:
            if c % 3 == 0 and c != 0:
                m += '-'
            c += 1
            m += str(t)

        db.set_snils(message.from_user.id, m)
        await message.answer("Вы успешно привязали снилс")
        await message.answer("Выберите направление, в рейтинге которого вы бы хотели узнать свое место", reply_markup=kb.Dir_kb)
    else:
        await message.answer("Не удалось распознать команду")


# Рассылка
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        subscriptions = db.get_subscriptions()
        for s in subscriptions:
            await bot.send_message(s[1], "position")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(3000))
    executor.start_polling(dp, skip_updates=True)
