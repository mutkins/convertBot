from dotenv import load_dotenv
import random
load_dotenv()
import uuid
import logging
import os, glob

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def get_lc_file_path(lc_filepath=None):
    # If there is a lc_filepath - use its name for folder, else use random (guid) name
    return f".\\temp\\{lc_filepath}\\" if lc_filepath else f".\\temp\\{uuid.uuid4()}\\"


async def get_tg_file_path(bot, file_id) -> str:
    file = await bot.get_file(file_id)
    filepath = file.file_path
    return filepath


async def download_file(bot, file_id, file_name) -> str:
    file_name = await replace_spaces(file_name)
    file_path = await get_tg_file_path(bot, file_id)
    destination = await get_lc_file_path()
    lc_file_path = await bot.download_file(file_path=file_path, destination=destination + file_name)
    return destination.split(sep='\\')[-2]


async def download_files(bot, file_id, file_name, lc_filepath=None) -> str:
    file_name = await replace_spaces(file_name)
    file_path = await get_tg_file_path(bot, file_id)
    destination = await get_lc_file_path(lc_filepath)
    lc_file_path = await bot.download_file(file_path=file_path, destination=destination + file_name)
    return lc_file_path.name


async def replace_spaces(_: str):
    return _.replace(' ', '_')


async def get_filepaths_from_folder(folder_name, format):
    return glob.glob(f'temp\\{folder_name}\\*.{format}')


class UploadFile:
    def __init__(self, filename):
        self.filname = filename

    def __enter__(self):
        self.file = open(self.filname, 'rb')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
