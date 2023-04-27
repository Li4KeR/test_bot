import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.dispatcher.filters import Text

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton
from aiogram.utils import executor

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from contextlib import suppress

from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound)

from keyboards import *
from sql_logic import check_sql


token = '6161217114:AAFeSrYVhOx7is3vJiLYADJet6eiCxbO34Q'
# logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", filename=log_path, )
logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
bot = Bot(token=token)
dp = Dispatcher(bot)


class NewSales(StatesGroup):
    id = State()                # Телеграм ID
    service = State()           # Услуга
    date = State()              # Дата записи
    master = State()            # Мастер
    payment = State()           # Оплата


@dp.message_handler(commands="start")
async def start(message: types.Message):
    """Стартовое меню"""
    await message.answer(
        text="Вас приветствует салон красоты Аврора!\n"
             "Выберите тему обращения:", reply_markup=main_menu)


@dp.callback_query_handler(lambda call: "main_menu" in call.data)
async def next_keyboard(call: types.CallbackQuery):
    """Возвращение в главное меню"""
    await call.message.edit_text(
        text="Вас приветствует салон красоты Аврора!\n"
             "Выберите тему обращения:"
    )
    await call.message.edit_reply_markup(reply_markup=main_menu)
    await call.answer()


""" test all masters menu """
@dp.callback_query_handler(Text(startswith="service"))
async def service(call: types.CallbackQuery, state: FSMContext):
    """меню с информацией мастера ногтей"""
    service_name = call.data.split("_")[1]
    menu = types.InlineKeyboardMarkup(row_width=2)
    all_services = get_all_services(service_name)
    for service_name, service_cb_name in all_services:
        menu.add(InlineKeyboardButton(text=f"{service_name}", callback_data=f"{service_cb_name}"))

    await state.update_data(service=f"{service_name}")
    await call.message.edit_text(text=f"Выберете услугу {service_name}")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()





if __name__ == '__main__':
    check_sql()
    executor.start_polling(dp, skip_updates=True)

# if __name__ == "__main__":
#     asyncio.run(main())