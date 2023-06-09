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


async def do_convert_video_folder(folder_name, target_format, message: types.Message):
    """This func convert all files target_format in folder_name and put new files in same folder"""
    file_num = 0
    file_paths = await get_filepaths_from_folder(folder_name=folder_name, file_format='*')
    files_total = len(file_paths)
    for source_file_path in file_paths:
        file_num += 1
        await do_convert_video_file(source_file_path=source_file_path, target_format=target_format, message=message, file_num=file_num, files_total=files_total)


async def do_convert_video_file(source_file_path, target_format, message: types.Message, file_num, files_total):
    result_file_path = source_file_path.split(sep='.')[-2] + f'.{target_format}'
    a = datetime.now()
    print(f'Started at {a}')
    log.info(f'Started converting file {source_file_path} to {target_format}')
    progress_text = f'Файл {file_num} из {files_total}'
    print(progress_text, end='')
    from handlers.covnert import send_progress_message
    progress_msg = await send_progress_message(message=message, text='Work in progress')
    try:
        result = subprocess.Popen(f'echo y | ffmpeg -loglevel warning -i {source_file_path} {result_file_path}',
                                  shell=True, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, encoding='utf-8')
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
            print(f'\nDone for {datetime.now() - a}.  Exited with returncode {result.returncode}')
            log.info(f'Done for {datetime.now() - a}.  Exited with returncode {result.returncode}')
    except ImagickException as e:
        print(f"EXCEPTION_TEXT={e}")
        log.error(e)
        raise Exception(e)















# async def do_convert_video_folder(folder_name, target_format):
#     """This func convert all files target_format in folder_name and put new files in same folder"""
#     for source_file_path in await get_filepaths_from_folder(folder_name=folder_name, file_format='*'):
#         result_file_path = source_file_path.split(sep='.')[-2] + f'.{target_format}'
#         async_converting_manager(source_file_path=source_file_path, result_file_path=result_file_path)
#
#
# def async_converting_manager(source_file_path, result_file_path):
#     main_loop = asyncio.get_event_loop()
#     main_loop.run_until_complete(asyncio.wait_for(async_converting(source_file_path=source_file_path, result_file_path=result_file_path, main_loop=main_loop),1000))
#
#
#
# async def progress_bar():
#     print('Work in progress', end='')
#     while True:
#         print('.', end='')
#         await asyncio.sleep(1)
#
#
# async def async_converting(source_file_path, result_file_path, main_loop):
#     try:
#         result = await asyncio.create_subprocess_shell(f'echo y | ffmpeg -i {source_file_path} {result_file_path}',
#                                                        stderr=asyncio.subprocess.PIPE)
#         main_loop.create_task(progress_bar())
#
#         await result.wait()
#         main_loop.close()
#         if result.returncode:
#             raise ImagickException(message=result.stderr)
#         else:
#             pass
#     except ImagickException as e:
#         log.error(e)
#         raise Exception(e)