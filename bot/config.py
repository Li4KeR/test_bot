import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


# token = '6161217114:AAFeSrYVhOx7is3vJiLYADJet6eiCxbO34Q'
token = '6161217114:AAFeSrYVhOx7is3vJiLYADJet6eiCxbO34Q'
# logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", filename=log_path, )
logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
bot = Bot(token=token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())