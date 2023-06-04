from aiogram import types
from aiogram.types import InlineKeyboardButton
from sql_logic import *


def create_main_menu():
    """ создание главного меню """
    menu = types.InlineKeyboardMarkup(row_width=2)
    # caterogies = sql_get_all_category()
    # menu.add(*[InlineKeyboardButton(button[1], callback_data=f"category_{button[0]}") for button in caterogies])
    menu.add(InlineKeyboardButton(text="Категории", callback_data="categories"),
             InlineKeyboardButton(text="Инфо о салоне", callback_data="main_info"),
             InlineKeyboardButton(text="Мои записи", callback_data="AllMyReg"))
    return menu


def create_menu_all_reg(id_telegram):
    """ создание меню с записями клиента """
    id_client = sql_get_id_client(id_telegram)[0]
    all_my_reg = sql_get_all_reg_client(id_client)
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        *[InlineKeyboardButton(button[1], callback_data=f"MyReg_{button[0]}") for button in all_my_reg])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    return menu


def create_menu_my_theat(id_reg):
    """ полная информация о записи """
    date, id_master, id_service = sql_get_all_info_reg(id_reg)
    master_name = sql_get_name_master(id_master)[0]
    service_name = sql_get_name_service(id_service)
    price = sql_get_price(id_service)[0]
    return date, master_name, service_name, price


def create_menu_caterory():
    """ создание меню с категориями """
    menu = types.InlineKeyboardMarkup(row_width=2)
    categories = sql_get_all_category()
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"category_{button[0]}") for button in categories])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    return menu


def create_menu_service(id_category):
    """ создание меню услуг с нужной категорией """
    menu = types.InlineKeyboardMarkup(row_width=2)
    category_name = sql_get_name_cat(id_category)
    services = sql_get_all_services(id_category)
    print(services)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"service_{button[0]}") for button in services])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    return menu, category_name


def create_menu_masters(id_service):
    """ создание меню мастеров с нужной услугой """
    menu = types.InlineKeyboardMarkup(row_width=2)
    name_service = sql_get_name_service(id_service)
    print(id_service)
    masters = sql_get_service_master(id_service)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"master_{button[0]}") for button in masters])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    return menu, name_service


def create_back_to_main():
    """ возврат в главное меню """
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    )
    return menu

