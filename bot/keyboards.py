from aiogram import types
from aiogram.types import InlineKeyboardButton


main_menu = types.InlineKeyboardMarkup(row_width=2)

#############################
cancel_board = types.InlineKeyboardMarkup(row_width=2)
cancel_board.add(
    InlineKeyboardButton(text="Главное меню", callback_data="main")
)
############################

main_menu.add(
    InlineKeyboardButton(text="Ногти", callback_data="service_nails"),
    InlineKeyboardButton(text="Брови", callback_data="service_brows"),
    InlineKeyboardButton(text="Парикмахер", callback_data="service_hair"),
    InlineKeyboardButton(text="Инфо о салоне", callback_data="main_info"),
    InlineKeyboardButton(text="Мои записи", callback_data="main_archive")
    # InlineKeyboardButton(text="Узнать об акциях клиники", url="https://moscowclinic.ru/offers")
)



