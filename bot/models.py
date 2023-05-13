from aiogram.dispatcher.filters.state import State, StatesGroup


class NewSales(StatesGroup):
    telegram_id = State()           # Телеграм ID
    category = State()              # Категория
    service = State()               # Услуга
    date = State()                  # Дата записи
    master = State()                # Мастер
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
