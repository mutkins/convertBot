from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboards
from create_bot import bot
import logging
from tools import download_file, get_filepaths_from_folder, is_asked, mark_asked, do_archive_files, mutate_message
from datetime import datetime
from handlers.common import send_welcome, reset_state
from converter import do_convert_folder


log = logging.getLogger("main")


class MyFSM(StatesGroup):
    waiting_file = State()
    waiting_format = State()


async def start_img(message: types.Message, state: FSMContext):
    await reset_state(state=state)
    async with state.proxy() as data:
        data['convert_type'] = 'img'
        log.info(f"Conversation start, convert type = {data.get('convert_type')}")
    await asking_file(message=message, state=state)


async def start_vid(message: types.Message, state: FSMContext):
    await reset_state(state=state)
    async with state.proxy() as data:
        data['convert_type'] = 'vid'
        log.info(f"Conversation start, convert type = {data.get('convert_type')}")
    await asking_file(message=message, state=state)


async def asking_file(message: types.Message, state: FSMContext):
    await message.answer("Отправьте файл для конвертации (не более 10 шт за раз)", parse_mode="HTML")
    await MyFSM.waiting_file.set()


async def taking_file(message: types.Message, state: FSMContext):
    mutate_message(message)
    if message.content_type == 'document' or message.content_type == 'video':
        print(f'{datetime.now()} пришел файл {message.content_name} media group id = {message.media_group_id}')
        log.info(f'User sent file {message.content_name} media group id = {message.media_group_id}')
        await download_document(message, state)
    else:
        await send_err_incorrect_frmt(message=message, state=state)


async def download_document(message: types.Message, state: FSMContext):
    log.info(f'Start downloading {message.content_name} media group id = {message.media_group_id}')

    async with state.proxy() as data:
        try:
            await message.answer(f"Скачиваю файл {message.content_name}")
            data['folder_name'] = await download_file(bot=bot, file_id=message.content_id,
                                                    file_name=message.content_name,
                                                    lc_filepath=message.media_group_id)

            log.info(f'Downloaded file {message.content_name} media group id = {message.media_group_id}')

        except Exception as e:
            log.info(f'Error when downloading file {message.content_name} media group id = {message.media_group_id}')
            await message.answer(e)
            raise Exception
    # Check:
    # 1. message 'ask_format' hasn't been sent yet,
    # 2. There are no files .pydownload (downloading yet) in the folder
    if is_asked(folder_name=data['folder_name']) or await get_filepaths_from_folder(folder_name=data['folder_name'], file_format='pydownload'):
        pass
    else:
        mark_asked(folder_name=data['folder_name'])
        await ask_format(message=message, state=state)


async def ask_format(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            log.info(f"SENDING Choose format message to user. Convert type = {data.get('convert_type')}")
            await message.answer("Выберите целевой формат", reply_markup=keyboards.get_formats_kb(convert_type=data.get('convert_type')))
        except Exception as e:
            log.error(e)
            await message.answer(e)
    await MyFSM.waiting_format.set()


async def convert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data.get('convert_type') == 'img':
            await convert_image(message=message, state=state)
        elif data.get('convert_type') == 'vid':
            await convert_video(message=message, state=state)
        else:
            raise Exception


async def convert_image(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['target_format'] = message.text
        try:
            log.info(f"START CONVERTING folder_name= {data['folder_name']}, target_format={data['target_format']}")
            await do_convert_folder(convert_type='img', folder_name=data['folder_name'], target_format=data['target_format'], message=message)
            log.info(f"SUCCESS CONVERTING folder_name= {data['folder_name']}, target_format={data['target_format']}")
        except Exception as e:
            await message.answer(e)
            await send_welcome(message=message, state=state)
            raise Exception
    await send_converted_file(message=message, state=state)


async def convert_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['target_format'] = message.text
        try:
            log.info(f"START CONVERTING folder_name= {data['folder_name']}, target_format={data['target_format']}")

            await do_convert_folder(convert_type='vid', folder_name=data['folder_name'], target_format=data['target_format'], message=message)
            log.info(f"SUCCESS CONVERTING folder_name= {data['folder_name']}, target_format={data['target_format']}")
        except Exception as e:
            await message.answer(e)
            await send_welcome(message=message, state=state)
            raise Exception
    await send_converted_file(message=message, state=state)


async def send_converted_file(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            file_list = await get_filepaths_from_folder(folder_name=data['folder_name'], file_format=data['target_format'])
            media = types.MediaGroup()
            if len(file_list) <= 10:
                for img in file_list:
                    media.attach_document(types.InputFile(img))

            else:
                archive_path = do_archive_files(file_list=file_list, folder_name=data['folder_name'])
                media.attach_document(types.InputFile(archive_path))
            await message.answer_media_group(media=media)
        except Exception as e:
            await message.answer(e)
            await send_welcome(message=message, state=state)
            raise Exception
    await state.finish()


async def send_err_incorrect_frmt(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, пришлите изображение как файл')


async def send_progress_message(message: types.Message, text, progress_msg=None):
    if progress_msg is None:
        progress_msg = await message.answer(text)
    else:
        progress_msg = await progress_msg.edit_text(text)
    return progress_msg


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_img, commands=['convert_img'], state='*')
    dp.register_message_handler(start_vid, commands=['convert_vid'], state='*')
    dp.register_message_handler(taking_file, state=MyFSM.waiting_file, content_types='any')
    dp.register_message_handler(convert, state=MyFSM.waiting_format)


