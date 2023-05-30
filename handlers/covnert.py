from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboards
from create_bot import dp, bot
import logging
from converters import do_convert_folder
from tools import download_file, get_filepaths_from_folder, is_asked, mark_asked
from datetime import datetime
from handlers.common import send_welcome, reset_state

log = logging.getLogger("main")


class MyFSM(StatesGroup):
    waiting_file = State()
    waiting_format = State()


async def asking_file(message: types.Message, state: FSMContext):
    await reset_state(state=state)
    await message.answer("Отправьте файл для конвертации", parse_mode="HTML")
    await MyFSM.waiting_file.set()


async def taking_file(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        print(f'{datetime.now()} пришел файл {message.document.file_name} media group id = {message.media_group_id}')
        await download_img(message, state)
    else:
        await send_err_incorrect_frmt(message, state)


async def download_img(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['folder_name'] = await download_file(bot=bot, file_id=message.document.file_id,
                                                  file_name=message.document.file_name,
                                                  lc_filepath=message.media_group_id)
    if is_asked(folder_name=data['folder_name']):
        pass
    else:
        mark_asked(folder_name=data['folder_name'])
        await ask_format(message, state)


async def ask_format(message: types.Message, state: FSMContext):
    await message.answer("Выберите целевой формат", reply_markup=keyboards.get_formats_kb())
    await MyFSM.waiting_format.set()


async def return_converted_file(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['target_format'] = message.text
        try:
            do_convert_folder(folder_name=data['folder_name'], target_format=data['target_format'])
        except Exception as e:
            await message.answer(e)
            await send_welcome(message=message, state=state)
            raise Exception
        media = types.MediaGroup()
        for img in await get_filepaths_from_folder(folder_name=data['folder_name'], file_format=data['target_format']):
            media.attach_document(types.InputFile(img))
    await message.answer_media_group(media=media)
    await state.finish()


async def send_err_incorrect_frmt(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, пришлите изображение как файл')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(asking_file, commands=['convert'], state='*')
    dp.register_message_handler(taking_file, state=MyFSM.waiting_file, content_types='any')
    dp.register_message_handler(return_converted_file, state=MyFSM.waiting_format)


