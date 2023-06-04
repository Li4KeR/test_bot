from aiogram import types
from aiogram.types import InlineKeyboardButton
from sql_logic import *


def create_menu_admin():
    """ создание меню админа """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Добавить", callback_data="AdminAdd"),
        # InlineKeyboardButton(text="Посмотреть", callback_data="AdminSelect"),
        InlineKeyboardButton(text="Удалить или изменить", callback_data="AdminDelete"),
        InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain")
    )
    return menu


def create_menu_return_main_admin():
    """ создание меню для возврата """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain")
    )
    return menu


def create_menu_add_admin():
    """ создание меню админа для удаления """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Добавить мастера", callback_data="AddMaster"),
        InlineKeyboardButton(text="Добавить категорию", callback_data="AddCategory"),
        InlineKeyboardButton(text="Добавить услугу", callback_data="AddService"),
        InlineKeyboardButton(text="Добавить связь", callback_data="AddRelation")
    )
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain"))
    return menu


def create_menu_relation_admin():
    """ создание меню связей """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Связать услугу и категорию", callback_data="addService_relation"),
        InlineKeyboardButton(text="Связать мастера и услугу", callback_data="addMaster_relation")
    )
    return menu


def create_menu_relation_old_category():
    """ создание меню выбора всех категорий для связей """
    menu = types.InlineKeyboardMarkup(row_width=2)
    all_cat = sql_get_all_category()
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"AllCategoryForRelation_{button[0]}")
               for button in all_cat],
             InlineKeyboardButton(text="Без категории", callback_data="CreateNewRelationService"))
    return menu


def create_menu_relation_old_category_service(category_id):
    """ создание меню выбора всех услуг в выбранной категории """
    all_services = sql_get_all_services(category_id)
    print(all_services)
    if all_services == []:
        check = False
    else:
        check = True
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"AllServicesInCategoryRelation_{button[0]}")
               for button in all_services])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain"))
    return menu, check


def create_menu_relation_all_category():
    """ создание меню выбора всех услуг в выбранной категории """
    all_category = sql_get_all_category()
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"RelationServiceDone_{button[0]}")
               for button in all_category])
    return menu


def create_menu_alone_services():
    """ создание меню всех услуг без категорий """
    all_services = sql_get_all_alone_service()
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"AllAloneServices_{button[0]}")
               for button in all_services])
    return menu


def create_menu_alone_categories(service_id):
    """ создание меню всех категорий """
    all_categories = sql_get_all_category()
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"AllAloneCategories_{button[0]}_{service_id}")
               for button in all_categories]
             )
    return menu


def create_menu_all_masters():
    """ создание меню с выюором мастеров """
    all_master = sql_get_all_masters()
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"RelationMaster_{button[0]}")
               for button in all_master]
             )
    return menu


def create_menu_all_cat_for_master():
    """ создание меню с выбором категории для мастера """
    all_category = sql_get_all_category()
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"RelationCatMaster_{button[0]}")
               for button in all_category]
             )
    return menu


def create_menu_all_master_service(category_id):
    """ создание меню с выбором услуги для мастера """
    all_services = sql_get_all_services(category_id)
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"RelationServiceMaster_{button[0]}")
               for button in all_services]
             )
    return menu


def create_menu_select_admin():
    """ создание меню админа для просмотра """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Глянуть мастеров", callback_data="AdminMasterSelect"),
        InlineKeyboardButton(text="Глянуть услуги", callback_data="AdminServiceSelect"),
        InlineKeyboardButton(text="Глянуть клиентов", callback_data="AdminClientsSelect"),
        InlineKeyboardButton(text="Глянуть записи", callback_data="AdminRegSelect")
    )
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain"))
    return menu


def create_menu_delete_admin():
    """ создание меню админа для удаления """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Удалить мастера", callback_data="AdminMasterDelete"),
        InlineKeyboardButton(text="Удалить услугу", callback_data="DeleteServiceAdmin"),
        InlineKeyboardButton(text="Удалить категорию", callback_data="DeleteCategoryAdmin"),
        InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain")
    )
    return menu


def create_menu_main_master_delete_admin():
    """ создание меню выбора удаления мастера """
    all_masters = sql_get_all_masters()
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"DeleteMaster_{button[0]}")
               for button in all_masters],
             InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain")
             )
    return menu


def create_menu_master_delete_admin(master_id):
    """ Меню инфы о мастере и выбор что сделать """
    master_info = sql_get_info_master(master_id)
    master_name = master_info[0]
    master_description = master_info[1]
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Удалить", callback_data=f"DeleteBDMaster_{master_id}"),
        InlineKeyboardButton(text="Изменить", callback_data=f"EditBDMaster_{master_id}"),
        InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain")
    )
    return menu, master_name, master_description


def create_main_menu_service_delete_admin():
    """ Создание меню всех услуг для удаления """
    all_services = sql_get_all_services_noid()
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"DeleteService_{button[0]}")
               for button in all_services],
             InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain")
             )
    return menu


def create_menu_service_delete_admin(service_id):
    """ Меню инфы об услуге и выбор что сделать """
    service_info = sql_get_all_info_service(service_id)
    print(service_info)
    service_name = service_info[0]
    service_price = service_info[1]
    service_time = service_info[2]
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Удалить", callback_data=f"DeleteBDService_{service_id}"),
        InlineKeyboardButton(text="Изменить", callback_data=f"EditBDService_{service_id}"),
        InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain")
    )
    return menu, service_name, service_price, service_time


def create_main_menu_category_delete_admin():
    """ Создание меню всех категорий для удаления """
    all_categorry = sql_get_all_category()
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"DeleteCategory_{button[0]}")
               for button in all_categorry],
             InlineKeyboardButton(text="Главное меню", callback_data="ADMINmain")
             )
    return menu

