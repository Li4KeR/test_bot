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
             InlineKeyboardButton(text="Мои записи", callback_data="main_archive"))
    return menu


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
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"service_{id_category}_{button[0]}") for button in services])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    return menu, category_name


def create_menu_masters(id_service):
    """ создание меню мастеров с нужной услугой """
    menu = types.InlineKeyboardMarkup(row_width=2)
    name_service = sql_get_name_service(id_service)
    masters = sql_get_service_master(id_service)
    menu.add(*[InlineKeyboardButton(button[1], callback_data=f"master_{button[0]}") for button in masters])
    menu.add(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    return menu, name_service










