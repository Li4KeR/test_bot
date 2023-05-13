from aiogram import types
from aiogram.types import InlineKeyboardButton
from sql_logic import *


def create_menu_admin():
    """ создание меню админа """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Добавить", callback_data="admin_add"),
        InlineKeyboardButton(text="Посмотреть", callback_data="admin_select"),
        InlineKeyboardButton(text="Удалить\редактировать", callback_data="admin_delete"),
        InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    )
    return menu


def create_menu_add_admin():
    """ создание меню админа для удаления """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Добавить мастера", callback_data="add_master"),
        InlineKeyboardButton(text="Добавить категорию", callback_data="add_category"),
        InlineKeyboardButton(text="Добавить услугу", callback_data="add_service"),
        InlineKeyboardButton(text="Добавить связь", callback_data="add_relation")
    )
    return menu


def create_menu_relation_admin():
    """ создание меню связей """
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(
        InlineKeyboardButton(text="Услуга - категории", callback_data="add_relation_sc"),
        InlineKeyboardButton(text="Мастер - услуга", callback_data="add_relation_ms")
    )
# def create_menu_add_admin_master():
#     """ создание меню для добавления мастера """
#     menu = types.InlineKeyboardMarkup(row_width=2)
#     menu.add(
#         InlineKeyboardButton(text="Добавить мастера", callback_data="admin_add_master"),
#         InlineKeyboardButton(text="Добавить категорию", callback_data="admin_add_category"),
#         InlineKeyboardButton(text="Добавить услугу", callback_data="admin_add_service"),
#         InlineKeyboardButton(text="Добавить_somethink_else", callback_data="admin_add_other")
#     )

