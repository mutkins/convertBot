import subprocess
import os
import logging
from dotenv import load_dotenv
from my_exceptions import ImagickException
from tools import get_filepaths_from_folder
import asyncio
from threading import Thread
import time
from datetime import datetime
from aiogram import types


log = logging.getLogger("main")
load_dotenv()

ffmpeg_path = os.environ.get('ffmpeg_path')
imagick_path = os.environ.get('imagick_path')


async def do_convert_folder(convert_type, folder_name, target_format, message: types.Message):
    from handlers.covnert import send_progress_message
    """This func convert all files target_format in folder_name and put new files in same folder"""
    file_num = 0
    file_paths = await get_filepaths_from_folder(folder_name=folder_name, file_format='*')
    files_total = len(file_paths)

    progress_msg = await send_progress_message(message=message, text='Work in progress')
    for source_file_path in file_paths:
        file_num += 1
        await do_convert_file(convert_type=convert_type, source_file_path=source_file_path, target_format=target_format, message=message, file_num=file_num, files_total=files_total, progress_msg=progress_msg)


# Это всё надо переписать. слишком нагромождено, нужно разбить на разные функции. Плюс, надо чтобы настрйоки генерации
# передавались удобнее, а не "если гиф - то фпс 10). Ну и "если линукс, то..." - тоже отстой
async def do_convert_file(convert_type, source_file_path, target_format, message: types.Message, file_num, files_total, progress_msg):
    from handlers.covnert import send_progress_message

    result_file_path = source_file_path.split(sep='.')[-2] + f'.{target_format}'
    log.info(f'Started converting file {source_file_path} to {target_format}')
    progress_text = f'Файл {file_num} из {files_total}'

    try:
        log.info(f'Started converting file {source_file_path} to {target_format}')
        if convert_type == 'vid':
            if target_format =='gif':
                result = subprocess.Popen(f'echo y | ffmpeg -loglevel warning -i {source_file_path} -filter:v fps=10 {result_file_path}',
                                      shell=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, encoding='utf-8')
            else:
                result = subprocess.Popen(f'echo y | ffmpeg -loglevel warning -i {source_file_path} {result_file_path}',
                                          shell=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL,
                                          encoding='utf-8')
        elif convert_type == 'img':
            # result = subprocess.Popen(f'{imagick_path} convert {source_file_path} {result_file_path}', # windows
            #                           stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
            result = subprocess.Popen(f'{imagick_path} convert {source_file_path} {result_file_path}', # windows
                                      stderr=subprocess.PIPE, stdout=subprocess.DEVNULL) # linux
        else:
            raise Exception
        while result.poll() is None:
            progress_text += '.'
            await send_progress_message(message=message, text=progress_text, progress_msg=progress_msg)
            print('.', end='')
            time.sleep(1)
        if result.returncode:
            progress_text += ' ОШИБКА'
            await send_progress_message(message=message, text=progress_text, progress_msg=progress_msg)
            err_msg = result.stderr.read()
            log.error(err_msg)
            raise ImagickException(message=err_msg)
        else:
            progress_text += ' ГОТОВО'
            await send_progress_message(message=message, text=progress_text, progress_msg=progress_msg)
    except ImagickException as e:
        print(f"EXCEPTION_TEXT={e}")
        log.error(e)
        raise Exception(e)








# THIS func for imgs works faster because package job mogrify, but it less usability, user dont get messages about progress for each file.
async def do_convert_folder_old(folder_name, target_format, message):
    """This func convert all files target_format in folder_name and put new files in same folder"""
    try:
        # result = subprocess.run(f'mogrify -format {target_format} temp/{folder_name}/*.*', capture_output=True, shell=True)  # FOR LINUX
        result = subprocess.run(f'{imagick_path} mogrify -format {target_format} temp/{folder_name}/*.*',
                                capture_output=True)  # FOR WINDOWS
        if result.stderr:
            raise ImagickException(message=result.stderr)
        else:
            return None
    except ImagickException as e:
        log.error(e)
        raise Exception(e)


# this reserve video converter just in case
async def do_convert_video_folder_old(folder_name, target_format):
    """This func convert all files target_format in folder_name and put new files in same folder"""
    for source_file_path in await get_filepaths_from_folder(folder_name=folder_name, file_format='*'):
        result_file_path = source_file_path.split(sep='.')[-2] + f'.{target_format}'
        try:
            result = subprocess.run(f'{ffmpeg_path} -i {source_file_path} {result_file_path}', capture_output=True)
            if result.returncode:
                raise ImagickException(message=result.stderr)
            else:
                pass
        except ImagickException as e:
            log.error(e)
            raise Exception(e)