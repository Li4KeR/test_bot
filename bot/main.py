from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from aiogram.utils import executor

from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar

from keyboards import *
from config import *
from admin_kb import *
from models import *


@dp.message_handler(commands="start")
async def start(message: types.Message):
    """Стартовое меню"""
    main_menu = create_main_menu()
    await message.answer(
        text="Вас приветствует салон красоты Аврора!\n"
             "Выберите тему обращения:", reply_markup=main_menu)


@dp.callback_query_handler(lambda call: "main_menu" in call.data)
async def main_menu_cb(call: types.CallbackQuery):
    """Возвращение в главное меню"""
    main_menu = create_main_menu()
    await call.message.edit_text(
        text="Вас приветствует салон красоты Аврора!\n"
             "Выберите тему обращения:"
    )
    await call.message.edit_reply_markup(reply_markup=main_menu)
    await call.answer()


@dp.callback_query_handler(Text(startswith="categories"))
async def caterories_cb(call: types.CallbackQuery, state: FSMContext):
    """ меню всех категорий """
    menu = create_menu_caterory()
    await call.message.edit_text(text="Выберете категорию:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await state.update_data(telegram_id=call.from_user.id)
    await call.answer()


@dp.callback_query_handler(Text(startswith="category"))
async def services_cb(call: types.CallbackQuery, state: FSMContext):
    """ меню всех услуг в категории """
    id_cat = call.data.split("_")[1]
    menu, cat_name = create_menu_service(id_cat)
    await call.message.edit_text(text="Выберете услугу:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await state.update_data(category=cat_name[0])
    await call.answer()


@dp.callback_query_handler(Text(startswith="service"))
async def services_cb(call: types.CallbackQuery, state: FSMContext):
    """ меню всех мастеров с этой услугой """
    id_service = call.data.split("_")[1]
    menu, name_service = create_menu_masters(id_service)
    await call.message.edit_text(text="Выберете мастера:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await state.update_data(service=name_service[0])
    await call.answer()


@dp.callback_query_handler(Text(startswith="master"))
async def nav_cal_handler(call: types.CallbackQuery, state: FSMContext):
    """ календарь """
    id_master = call.data.split("_")[1]
    name_master = sql_get_name_master(id_master)
    await state.update_data(master=name_master[0])
    await call.message.edit_text(text="Выберете дату:")
    await call.message.edit_reply_markup(reply_markup=await SimpleCalendar().start_calendar())
    # await call.answer("Please select a date: ", reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """ отлов событий на календаре """
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    await state.update_data(date=date)
    data = await state.get_data()
    print(data['telegram_id'])
    print(data['category'])
    print(data['service'])
    print(data['master'])
    if selected:
        # await callback_query.message.answer(
        #     f'Вы записались к {data["master"]}\n'
        #     f'На услугу {data["service"]}\n'
        #     f'Дата: {data["date"].strftime("%d.%m.%Y")}',
        #     reply_markup=create_main_menu()
        # )
        await callback_query.message.answer(text="Введите Ваши ФИО", reply_markup=create_main_menu())
        await NewSales.client_name.set()


@dp.message_handler(state=NewSales.client_name)
async def enter_phones(message: types.Message, state: FSMContext):
    """ отлов события ввода имени, фсм в стейт phone """
    # await state.update_data(id=message.from_user.id)
    await state.update_data(client_name=message.text)
    await message.answer('Введите Ваш номер телефона')
    await NewSales.phone.set()


@dp.message_handler(state=NewSales.phone)
async def enter_phones(message: types.Message, state: FSMContext):
    """ отлов события ввода телефона и добавление записи в бд """
    # await state.update_data(id=message.from_user.id)
    await state.update_data(phone=message.text)
    data = await state.get_data()
    await state.finish()
    if data["telegram_id"] = []:
        create_client()
    else:
        pass



""" ---------------- admin -----------------"""


@dp.message_handler(commands="admin")
async def admin(message: types.Message):
    """ меню админа"""
    main_menu = create_menu_admin()
    await message.answer(
        text="Салют, админ!\n"
             "Выберите что посмотреть\исправить\добавить:", reply_markup=main_menu)


@dp.callback_query_handler(lambda call: "admin_add" in call.data)
async def admin_add(call: types.CallbackQuery):
    """ меню добавление для админа """
    menu = create_menu_add_admin()
    await call.message.edit_text(text="Выбери, что хочешь добавить")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "add_master" in call.data)
async def admin_add_master(call: types.CallbackQuery, state: FSMContext):
    """ отлов события ввода имени мастера """
    await call.message.edit_text(text="Введи имя мастера")
    await state.set_state(AddMaster.name)
    await AddMaster.name.set()
    await call.answer()


@dp.message_handler(state=AddMaster.name)
async def enter_phones(message: types.Message, state: FSMContext):
    """ отлов события ввода описания мастера """
    # await state.update_data(id=message.from_user.id)
    await state.update_data(name=message.text)
    await message.answer('Введи описание для мастера')
    await AddMaster.description.set()


@dp.message_handler(state=AddMaster.description)
async def enter_phones(message: types.Message, state: FSMContext):
    """ добавление мастера в бд """
    await state.update_data(description=message.text)
    data = await state.get_data()
    await state.finish()
    sql_add_master(data['name'], data['description'])
    main_menu = create_menu_admin()
    await message.answer('мастер добавлен', reply_markup=main_menu)
    await AddMaster.description.set()


@dp.callback_query_handler(lambda call: "add_category" in call.data)
async def admin_add_category(call: types.CallbackQuery, state: FSMContext):
    """ добавитьб категорию """
    await call.message.edit_text(text="Введи имя категории")
    await state.set_state(AddCategory.name)
    await AddCategory.name.set()
    await call.answer()


@dp.message_handler(state=AddCategory.name)
async def admin_enter_cat_name(message: types.Message, state: FSMContext):
    """ добавление категории в бд """
    await state.update_data(name=message.text)
    main_menu = create_menu_admin()
    data = await state.get_data()
    await state.finish()
    sql_add_category(data['name'])
    await message.answer('Категория добавлена', reply_markup=main_menu)


@dp.callback_query_handler(lambda call: "add_service" in call.data)
async def admin_add_service(call: types.CallbackQuery, state: FSMContext):
    """ добавитьб сервис """
    await call.message.edit_text(text="Введи имя услуги")
    await state.set_state(AddService.name)
    await AddService.name.set()
    await call.answer()


@dp.message_handler(state=AddService.name)
async def add_service_name(message: types.Message, state: FSMContext):
    """ сохранить имя и добавить стоимость услуги """
    await state.update_data(name=message.text)
    await message.answer('Введите стоимость:')
    await AddService.price.set()


@dp.message_handler(state=AddService.price)
async def add_service_price(message: types.Message, state: FSMContext):
    """ сохранить стоимость добавить время услуги """
    await state.update_data(price=message.text)
    await message.answer('Введите время оказания услуги')
    await AddService.time.set()


@dp.message_handler(state=AddService.time)
async def admin_enter_cat_name(message: types.Message, state: FSMContext):
    """ добавление категории в бд """
    await state.update_data(time=message.text)
    main_menu = create_menu_admin()
    data = await state.get_data()
    await state.finish()
    sql_add_service(data['name'], data['price'], data['time'])
    await message.answer('Услуга добавлена', reply_markup=main_menu)


@dp.callback_query_handler(lambda call: "add_relation" in call.data)
async def admin_add(call: types.CallbackQuery):
    """ меню добавление связей для админа """
    menu = create_menu_relation_admin()
    await call.message.edit_text(text="Выбери, что хочешь добавить")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


if __name__ == '__main__':
    check_sql()
    executor.start_polling(dp, skip_updates=True)

# if __name__ == "__main__":
#     asyncio.run(main())
