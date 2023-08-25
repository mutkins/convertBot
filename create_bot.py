import os
from aiogram import Bot, Dispatcher, types
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

storage = MemoryStorage()
load_dotenv()


local_server = TelegramAPIServer.from_base('http://localhost:8008')
# Initialize bot and dispatcher
bot = Bot(token=os.environ.get('tgBot_id'), server=local_server)
dp = Dispatcher(bot, storage=storage)
