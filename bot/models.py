from aiogram.dispatcher.filters.state import State, StatesGroup


class NewSales(StatesGroup):
    telegram_id = State()           # Телеграм ID
    category = State()              # Категория
    service = State()               # Услуга
    id_service = State()            # Айди услуги
    date = State()                  # Дата записи
    master = State()                # Мастер
    id_master = State()             # Айди мастера
    payment = State()               # Оплата
    client_name = State()           # Имя клиента
    phone = State()                 # Телефон


class AddMaster(StatesGroup):
    name = State()                  # Имя мастера
    description = State()           # Описание для мастера


class AddCategory(StatesGroup):
    name = State()                  # Имя категории


class AddService(StatesGroup):
    name = State()                  # Имя услуги
    price = State()                 # Стоимость услуги
    time = State()                  # Время для оказания услуги


class AddRelation(StatesGroup):
    service_name = State()          # Имя услуги
    service_id = State()            # id услуги
    category_name = State()         # Имя категории
    category_id = State()           # id категории


class AddRelationMaster(StatesGroup):
    master_id = State()             #
    master_name = State()           #
    service_id = State()            #
    service_name = State()          #


class RenameMaster(StatesGroup):
    master_id = State()             #
    master_name = State()           #
    master_description = State()    #


class RenameService(StatesGroup):
    service_id = State()            #
    service_name = State()          #
    service_price = State()         #
    service_time = State()          #


