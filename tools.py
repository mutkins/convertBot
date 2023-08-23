import os
import shutil
from dotenv import load_dotenv
import uuid
import logging
import glob
from zipfile import ZipFile
from os.path import basename

load_dotenv()
log = logging.getLogger("main")


async def get_lc_file_path(lc_filepath=None):
    """This func generates local path for temporary files.
     If lc_filepath has given - use its name for folder, else use random (guid) name"""
    return f"./temp/{lc_filepath}/" if lc_filepath else f"./temp/{uuid.uuid4()}/"  # FOR LINUX
    # return f".\\temp\\{lc_filepath}\\" if lc_filepath else f".\\temp\\{uuid.uuid4()}\\" - for WINDOWS


async def get_tg_file_path(bot, file_id) -> str:
    """This func return system telegram filepath from file id"""
    file = await bot.get_file(file_id)
    filepath = file.file_path
    return filepath


async def download_file(bot, file_id, file_name, lc_filepath=None) -> str:
    """This func download file from tg server to the temporary folder on the local disk"""
    file_path = await get_tg_file_path(bot, file_id)
    destination = await get_lc_file_path(lc_filepath)
    # .pydownload - postfix to mark downloading files
    await bot.download_file(file_path=file_path, destination=destination + file_name + '.pydownload')
    # When download complete - remove .pydownload postfix
    await rename_aft_download(destination + file_name + '.pydownload')
    # return destination.split(sep='\\')[-2]  FOR WINDOWS
    return destination.split(sep='/')[-2]  # FOR LINUX


async def rename_aft_download(file_path):
    os.rename(file_path, file_path.rsplit(sep='.', maxsplit=1)[0])


async def get_filepaths_from_folder(folder_name, file_format):
    """This func return list names of files specified format which exist in folder"""
    # return glob.glob(f'temp\\{folder_name}\\*.{file_format}') FOR WINDOWS
    return glob.glob(f'temp/{folder_name}/*.{file_format}')  # FOR LINUX


def is_asked(folder_name):
    # return bool(glob.glob(f'temp\\{folder_name}\\_'))  FOR WINDOWS
    return bool(glob.glob(f'temp/{folder_name}/_'))  # FOR LINUX


def mark_asked(folder_name):
    # with open(f'temp\\{folder_name}\\_', 'w') as f:  FOR WINDOWS
    with open(f'temp/{folder_name}/_', 'w') as f:  # FOR LINUX
        pass


def do_archive_files(file_list, folder_name):
    zipfile_name = f'temp/{folder_name}/attachments.zip'
    with ZipFile(zipfile_name, 'w') as zipObj:
        # Add multiple files to the zip
        for img in file_list:
            zipObj.write(img, basename(img))
    return zipfile_name
