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


@dp.callback_query_handler(lambda call: "main_info" in call.data)
async def main_menu_cb(call: types.CallbackQuery):
    """ Инфо о салоне """
    main_menu = create_back_to_main()
    await call.message.edit_text(
        text="О нас: Салон красоты «AvRorrra»предлагает спектр услуг для красоты и здоровья, "
             "дарит радость и хорошее настроение)🌺✨\nНаш адрес: "
             "г. Москва, ул. Стромынка, 22. Телефон салона красоты +7(918)461-83-19"
    )
    await call.message.edit_reply_markup(reply_markup=main_menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "AllMyReg" in call.data)
async def main_menu_cb(call: types.CallbackQuery):
    """ Меню мои записи """
    id_telegram = call.from_user.id
    main_menu = create_menu_all_reg(id_telegram)
    await call.message.edit_text(
        text="Вот все твои записи:"
    )
    await call.message.edit_reply_markup(reply_markup=main_menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "MyReg" in call.data)
async def main_menu_cb(call: types.CallbackQuery):
    """ определенная запись клиента """
    id_reg = call.data.split("_")[1]
    main_menu = create_back_to_main()
    date, master, service, price = create_menu_my_theat(id_reg)
    await call.message.edit_text(
        text=f"Вы записаны к мастеру {master}\n"
             f"Дата: {date}\n"
             f"Услуга: {service}\n"
             f"Стоимость: {price}"
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
    await state.update_data(category=cat_name)
    await call.answer()


@dp.callback_query_handler(Text(startswith="service"))
async def services_cb(call: types.CallbackQuery, state: FSMContext):
    """ меню всех мастеров с этой услугой """
    id_service = call.data.split("_")[1]
    menu, name_service = create_menu_masters(id_service)
    await call.message.edit_text(text="Выберете мастера:")
    await call.message.edit_reply_markup(reply_markup=menu)
    await state.update_data(service=name_service)
    await state.update_data(id_service=id_service)
    await call.answer()


@dp.callback_query_handler(Text(startswith="master"))
async def nav_cal_handler(call: types.CallbackQuery, state: FSMContext):
    """ календарь """
    id_master = call.data.split("_")[1]
    name_master = sql_get_name_master(id_master)
    await state.update_data(master=name_master[0])
    await state.update_data(id_master=id_master)
    await call.message.edit_text(text="Выберете дату:")
    await call.message.edit_reply_markup(reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """ отлов событий на календаре """
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    await state.update_data(date=date)
    if selected:
        await callback_query.message.answer(text="Введите Ваши ФИО")  # , reply_markup=create_main_menu()
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
    tele_id = data["telegram_id"]
    category = data["category"]
    service = data["service"]
    id_service = data["id_service"]
    date = data["date"].strftime("%d.%m.%Y")
    master = data["master"]
    id_master = data["id_master"]
    client_name = data["client_name"]
    phone = data['phone']
    price = sql_get_price(id_service)[0]
    check_tele = sql_check_telegram(tele_id)
    menu = create_back_to_main()
    if check_tele == []:
        sql_add_client(tele_id, client_name, phone)
        id_client = sql_check_telegram(tele_id)[0][0]
    else:
        id_client = check_tele[0][0]
    sql_add_sale(id_master, id_client, id_service, date)
    await message.answer(text=f"Вы записаны к мастеру: {master}\n"
                              f"На услугу: {service}\n"
                              f"Дата: {date}\n"
                              f"Стоимость: {price}", reply_markup=menu)
    for operator in operators:
        urll = f"tg://user?id='{tele_id}'"
        cb = types.InlineKeyboardMarkup(row_width=1)
        cb.add(InlineKeyboardButton(text='Написать клиенту', url=urll))
        await bot.send_message(operator, f"Запись пользователя: {client_name}\n"
                                         f"Дата: {date}\n"
                                         f"Телефон: {phone}\n"
                                         f"К кому: {master}\n"
                                         f"Услуга: {service}\n"
                                         f"Стоимость: {price}", reply_markup=cb)



""" ---------------- admin -----------------"""


@dp.message_handler(commands="admin")
async def admin(message: types.Message):
    """ меню админа"""
    print(message.from_user.id)
    print(admins)
    if message.from_user.id in admins:
        main_menu = create_menu_admin()
        await message.answer(
            text="Салют, админ!\n"
                 "Выберите что посмотреть\исправить\добавить:", reply_markup=main_menu)
    else:
        await message.answer(
            text="Тебя нет в админке, пиши админу!", reply_markup=create_back_to_main())


@dp.callback_query_handler(lambda call: "ADMINmain" in call.data)
async def admin(call: types.CallbackQuery):
    """ меню админа"""
    main_menu = create_menu_admin()
    await call.message.edit_text(text="Салют, админ!\n"
                                      "Выберите что посмотреть\исправить\добавить:")
    await call.message.edit_reply_markup(reply_markup=main_menu)


@dp.callback_query_handler(lambda call: "AdminAdd" in call.data)
async def admin_add(call: types.CallbackQuery):
    """ меню добавление для админа """
    menu = create_menu_add_admin()
    await call.message.edit_text(text="Выбери, что хочешь добавить")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "AddMaster" in call.data)
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
    menu = create_menu_return_main_admin()
    await message.answer('мастер добавлен', reply_markup=menu)


@dp.callback_query_handler(lambda call: "AddCategory" in call.data)
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
    menu = create_menu_return_main_admin()
    data = await state.get_data()
    await state.finish()
    sql_add_category(data['name'])
    await message.answer('Категория добавлена', reply_markup=menu)


@dp.callback_query_handler(lambda call: "AddService" in call.data)
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
    menu = create_menu_return_main_admin()
    data = await state.get_data()
    await state.finish()
    sql_add_service(data['name'], data['price'], data['time'])
    await message.answer('Услуга добавлена', reply_markup=menu)


@dp.callback_query_handler(lambda call: "AddRelation" in call.data)
async def admin_add_relation(call: types.CallbackQuery):
    """ меню добавление связей для админа """
    menu = create_menu_relation_admin()
    await call.message.edit_text(text="Выбери, что хочешь связать")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "addService_relation" in call.data)
async def admin_add_relation_all_cat(call: types.CallbackQuery):
    """ меню выбора усдуги из категории для связи """
    menu = create_menu_relation_old_category()
    await call.message.edit_text(text="Выбери категорию")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


# @dp.callback_query_handler(lambda call: "AllCategoryForRelation")
@dp.callback_query_handler(lambda call: "AllCategoryForRelation" in call.data)
async def admin_add_relation_all_service_cat(call: types.CallbackQuery):
    """ меню выбора усдуг с выбранной категорией """
    id_category = call.data.split("_")[1]
    menu, check = create_menu_relation_old_category_service(id_category)
    print(menu)
    if check == False:
        await call.message.edit_text(text="В этой категории еще нет услуг")
        await call.message.edit_reply_markup(reply_markup=menu)
    else:
        await call.message.edit_text(text="Выбери услугу")
        await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "AllServicesInCategoryRelation" in call.data)
async def admin_add_relation_all_new_cat(call: types.CallbackQuery, state: FSMContext):
    """ меню выбора новой категории для услуги """
    service_id = call.data.split("_")[1]
    service_name = sql_get_name_service(service_id)
    menu = create_menu_relation_all_category()
    await state.update_data(service_name=service_name)
    await state.update_data(service_id=service_id)
    await call.message.edit_text(text="Выбери услугу")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "RelationServiceDone" in call.data)
async def admin_add_relation_service_done(call: types.CallbackQuery, state: FSMContext):
    """ Добавление связи в бд """
    data = await state.get_data()
    category_id = call.data.split("_")[1]
    category_name = sql_get_name_cat(category_id)
    service_id = data["service_id"]
    menu = create_menu_return_main_admin()
    await state.update_data(category_id=category_id)
    await state.update_data(category_name=category_name)
    await state.finish()
    sql_add_relation_services(category_id, service_id)
    await call.message.edit_text(text=f"Вы добавили {data['service_name']} к категории {data['category_name']}")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "CreateNewRelationService" in call.data)
async def admin_add_relation_all_new_cat(call: types.CallbackQuery):
    """ меню выбора услуги без категорий """
    menu = create_menu_alone_services()
    await call.message.edit_text(text="Выбери услугу")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "AllAloneServices" in call.data)
async def admin_add_relation_alone_service(call: types.CallbackQuery):
    """ меню выбора категории для услуги """
    service_id = call.data.split("_")[1]
    menu = create_menu_alone_categories(service_id)
    await call.message.edit_text(text="Выбери категорию")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "AllAloneCategories" in call.data)
async def admin_add_relation_alone_category(call: types.CallbackQuery):
    """ меню выбора категории для услуги """
    category_id = call.data.split("_")[1]
    service_id = call.data.split("_")[2]
    sql_add_relation_services(category_id, service_id)
    service_name = sql_get_name_service(service_id)
    category_name = sql_get_name_cat(category_id)
    menu = create_menu_return_main_admin()
    await call.message.edit_text(text=f"Услуга {service_name} добавлена в категорию {category_name}")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "addMaster_relation" in call.data)
async def create_menu_rel_master(call: types.CallbackQuery):
    """ меню выбора мастера для связи с услугой """
    menu = create_menu_all_masters()
    await call.message.edit_text(text=f"Выбери мастера")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "RelationMaster" in call.data)
async def create_menu_all_cat_masters(call: types.CallbackQuery, state: FSMContext):
    """ меню выбора категории для мастера """
    master_id = call.data.split("_")[1]
    menu = create_menu_all_cat_for_master()
    await state.update_data(master_id=master_id)
    await call.message.edit_text(text=f"Выбери категорию")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "RelationCatMaster" in call.data)
async def create_menu_all_service_masters(call: types.CallbackQuery, state: FSMContext):
    """ меню выбора услуги для мастера """
    category_id = call.data.split("_")[1]
    menu = create_menu_all_master_service(category_id)
    # await state.update_data(master_id=master_id)
    await call.message.edit_text(text=f"Выбери услугу")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "RelationServiceMaster" in call.data)
async def create_menu_skills_bd(call: types.CallbackQuery, state: FSMContext):
    """ запись скилов в бд """
    data = await state.get_data()
    await state.finish()
    service_id = call.data.split("_")[1]
    service_name = sql_get_name_service(service_id)
    master_id = data['master_id']
    master_name = sql_get_name_master(master_id)[0]
    menu = create_menu_return_main_admin()
    sql_add_relation_master(master_id, service_id)
    await call.message.edit_text(text=f"Вы добавили мастеру: {master_name}\n"
                                      f"услугу: {service_name}")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "AdminSelect" in call.data)
async def create_menu_select(call: types.CallbackQuery):
    """ Показ того, что можно посмотреть """
    menu = create_menu_select_admin()
    await call.message.edit_text(text="Что хочешь глянуть?")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "AdminDelete" in call.data)
async def create_menu_main_delete(call: types.CallbackQuery):
    """ Показ того, что можно удалить """
    menu = create_menu_delete_admin()
    await call.message.edit_text(text="Что хочешь удалить?")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "AdminMasterDelete" in call.data)
async def create_menu_delte_master(call: types.CallbackQuery):
    """ Показ всех мастеров для удаления """
    menu = create_menu_main_master_delete_admin()
    await call.message.edit_text(text="Какого мастера удалить?")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "DeleteMaster" in call.data)
async def create_menu_delte_master(call: types.CallbackQuery):
    """ Показ инфы о мастере и выбор что делать """
    master_id = call.data.split("_")[1]
    menu, master_name, master_description = create_menu_master_delete_admin(master_id)
    await call.message.edit_text(text=f"Что сделать с мастером {master_name}?\n"
                                      f"{master_description}")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "DeleteBDMaster" in call.data)
async def create_menu_delete_master_done(call: types.CallbackQuery):
    """ Удаление мастера из бд """
    master_id = call.data.split("_")[1]
    master_name = sql_get_name_master(master_id)[0]
    sql_delete_master(master_id)
    menu = create_menu_return_main_admin()
    await call.message.edit_text(text=f"Мастер {master_name} удален!")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "EditBDMaster" in call.data)
async def create_menu_delte_master_done(call: types.CallbackQuery, state: FSMContext):
    """ Редактирование мастера в бд """
    master_id = call.data.split("_")[1]
    master_name = sql_get_name_master(master_id)[0]
    await state.update_data(master_id=master_id)
    await call.message.edit_text(text=f"Выберете новое имя мастера!\n"
                                      f"Прошлое имя: {master_name}")
    # await call.message.edit_reply_markup(reply_markup=menu)
    await RenameMaster.master_name.set()
    await call.answer()


@dp.message_handler(state=RenameMaster.master_name)
async def enter_phones(message: types.Message, state: FSMContext):
    """ Запись имени и ожидание ввода описания """
    data = await state.get_data()
    master_id = data["master_id"]
    master_description = sql_get_info_master(master_id)[1]
    await state.update_data(master_name=message.text)
    await message.answer(f'Введите описание мастера!\n'
                         f'Старое описание: {master_description}')
    await RenameMaster.master_description.set()


@dp.message_handler(state=RenameMaster.master_description)
async def enter_descript_master(message: types.Message, state: FSMContext):
    """ Запись описания и изменение в бд """
    # await RenameMaster.master_description(message.text)
    await state.update_data(master_description=message.text)
    data = await state.get_data()
    await state.finish()
    master_id = data['master_id']
    master_name = data['master_name']
    master_description = data['master_description']
    old_data = sql_get_info_master(master_id)
    old_master_name = old_data[0]
    old_master_description = old_data[1]
    sql_edit_master(master_id, master_name, master_description)
    menu = create_menu_return_main_admin()
    await message.answer(text=f'Изменения мастера:\n'
                              f'Имя: {old_master_name} => {master_name}\n'
                              f'Описание: {old_master_description} = >{master_description}\n',
                         reply_markup=menu)


@dp.callback_query_handler(lambda call: "DeleteServiceAdmin" in call.data)
async def create_main_menu_delete_service(call: types.CallbackQuery):
    """ Показ всех услуг для удаления """
    menu = create_main_menu_service_delete_admin()
    await call.message.edit_text(text="Какую услугу удалить?")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "DeleteService" in call.data)
async def create_menu_delete_service(call: types.CallbackQuery):
    """ Показ всей инфы об услуге """
    service_id = call.data.split("_")[1]
    menu, service_name, service_price, service_time = create_menu_service_delete_admin(service_id)
    await call.message.edit_text(text=f"Услуга: {service_name}\n"
                                      f"Цена: {service_price}\n"
                                      f"Время: {service_time}")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "DeleteBDService" in call.data)
async def create_menu_delete_service_done(call: types.CallbackQuery):
    """ Удаление услуги из бд """
    service_id = call.data.split("_")[1]
    service_name = sql_get_name_service(service_id)
    sql_delete_service(service_id)
    menu = create_menu_return_main_admin()
    await call.message.edit_text(text=f"Услуга {service_name} удалена!")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "EditBDService" in call.data)
async def create_menu_delte_master_done(call: types.CallbackQuery, state: FSMContext):
    """ Редактирование услуги в бд """
    service_id = call.data.split("_")[1]
    old_service_name = sql_get_name_service(service_id)[0]
    await state.update_data(service_id=service_id)
    await call.message.edit_text(text=f"Введите новое имя для {old_service_name}!")
    # await call.message.edit_reply_markup(reply_markup=menu)
    await RenameService.service_name.set()
    await call.answer()


@dp.message_handler(state=RenameService.service_name)
async def enter_phones(message: types.Message, state: FSMContext):
    """ Запись имени и ожидание ввода описания """
    data = await state.get_data()
    service_id = data["service_id"]
    old_service_price = sql_get_price(service_id)
    await state.update_data(service_name=message.text)
    await message.answer(f'Введите новую цену для услуги {data["service_name"]}!\n'
                         f'Старая цена: {old_service_price}')
    await RenameService.service_time.set()


@dp.message_handler(state=RenameService.service_time)
async def enter_descript_master(message: types.Message, state: FSMContext):
    """ Запись времени и изменение в бд """
    await state.update_data(service_time=message.text)
    data = await state.get_data()
    await state.finish()
    service_id = data['service_id']
    service_name = data['service_name']
    service_price = data['service_price']
    service_time = data['service_time']
    old_data = sql_get_all_info_service(service_id)
    old_service_name = old_data[0]
    old_service_price = old_data[1]
    old_service_time = old_data[2]
    sql_edit_service(service_id, service_name, service_price, service_time)
    menu = create_menu_return_main_admin()
    await message.answer(text=f'Изменения услуги:\n'
                              f'Имя: {old_service_name} => {service_name}\n'
                              f'Цена: {old_service_price} => {service_price}\n'
                              f'Время: {old_service_time} => {service_time}',
                         reply_markup=menu)



@dp.callback_query_handler(lambda call: "DeleteCategoryAdmin" in call.data)
async def create_menu_delete_service(call: types.CallbackQuery):
    """ Показ всех категорий для удаления """
    menu = create_main_menu_category_delete_admin()
    await call.message.edit_text(text="Какую категорию удалить?")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "DeleteService" in call.data)
async def create_menu_delete_service(call: types.CallbackQuery):
    """ Показ всей инфы о категории """
    category_id = call.data.split("_")[1]
    category_name = sql_get_name_cat(category_id)
    menu = create_menu_caterory_delete_admin(category_id)
    # menu, service_name, service_price, service_time = create_menu_service_delete_admin(service_id)
    await call.message.edit_text(text=f"Категория: {category_name}\n")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


@dp.callback_query_handler(lambda call: "DeleteCategory" in call.data)
async def create_menu_delete_service_done(call: types.CallbackQuery):
    """ Удаление категории из бд """
    category_id = call.data.split("_")[1]
    category_name = sql_get_name_cat(category_id)
    sql_delete_category(category_id)
    menu = create_menu_return_main_admin()
    await call.message.edit_text(text=f"Категория {category_name} удалена!")
    await call.message.edit_reply_markup(reply_markup=menu)
    await call.answer()


if __name__ == '__main__':
    check_sql()
    executor.start_polling(dp, skip_updates=True)

# if __name__ == "__main__":
#     asyncio.run(main())
