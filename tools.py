from dotenv import load_dotenv
import uuid
import logging
import glob

load_dotenv()
log = logging.getLogger("main")


async def get_lc_file_path(lc_filepath=None):
    """This func generates local path for temporary files.
     If lc_filepath has given - use its name for folder, else use random (guid) name"""
    return f".\\temp\\{lc_filepath}\\" if lc_filepath else f".\\temp\\{uuid.uuid4()}\\"


async def get_tg_file_path(bot, file_id) -> str:
    """This func return system telegram filepath from file id"""
    file = await bot.get_file(file_id)
    filepath = file.file_path
    return filepath


async def download_file(bot, file_id, file_name, lc_filepath=None) -> str:
    """This func download file from tg server to the temporary folder on the local disk"""
    file_path = await get_tg_file_path(bot, file_id)
    destination = await get_lc_file_path(lc_filepath)
    await bot.download_file(file_path=file_path, destination=destination + file_name)
    return destination.split(sep='\\')[-2]


async def get_filepaths_from_folder(folder_name, file_format):
    """This func return list names of files specified format which exist in folder"""
    return glob.glob(f'temp\\{folder_name}\\*.{file_format}')


class UploadFile:
    def __init__(self, filename):
        self.filname = filename

    def __enter__(self):
        self.file = open(self.filname, 'rb')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
