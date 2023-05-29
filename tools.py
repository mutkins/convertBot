import os
from dotenv import load_dotenv
import random
load_dotenv()
import uuid
import logging

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def get_lc_file_path(dest):
    return f".\\temp\\{uuid.uuid4()}\\"


async def get_tg_file_path(bot, file_id) -> str:
    file = await bot.get_file(file_id)
    filepath = file.file_path
    return filepath


async def download_file(bot, file_id, file_name) -> str:
    file_name = await replace_spaces(file_name)
    file_path = await get_tg_file_path(bot, file_id)
    destination = await get_lc_file_path(dest='input')
    lc_file_path = await bot.download_file(file_path=file_path, destination=destination + file_name)
    return lc_file_path.name


async def replace_spaces(_: str):
    return _.replace(' ', '_')


class UploadFile:
    def __init__(self, filename):
        self.filname = filename

    def __enter__(self):
        self.file = open(self.filname, 'rb')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
