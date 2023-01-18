import config
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import DB

storage = MemoryStorage

bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DB.Database('db/TESTDB.db', users_table="people", catalog_table="catalog", cart_table="cart")

