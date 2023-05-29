import configparser
import logging
import os
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv
from create_bot import dp
from handlers import common, covnert

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


# Register handlers from handlers folder
common.register_handlers(dp)
covnert.register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
