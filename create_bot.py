import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

storage = MemoryStorage()
load_dotenv()

# Initialize bot and dispatcher
bot = Bot(token=os.environ.get('tgBot_id'))
dp = Dispatcher(bot, storage=storage)
