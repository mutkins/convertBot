import os

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import keyboards
from create_bot import dp, bot
import logging
import io
from converters import do_convert
from tools import download_file, UploadFile
from datetime import datetime
from handlers.common import send_welcome, reset_state


class MyFSM(StatesGroup):
    waiting_file = State()
    waiting_format = State()


async def asking_file(message: types.Message, state: FSMContext):
    await reset_state(state=state)
    await message.answer("Отправьте файл для конвертации", parse_mode="HTML")
    await MyFSM.waiting_file.set()


async def taking_file(message: types.Message, state: FSMContext):
    # print(f'{datetime.now()} пришел файл {message.document.file_name}')

    if message.content_type == 'document':
        await download_img(message, state)
    else:
        await send_err_incorrect_frmt(message, state)


async def download_img(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['input_filepath'] = await download_file(bot=bot, file_id=message.document.file_id,
                                                     file_name=message.document.file_name)
    await ask_format(message, state)


async def ask_format(message: types.Message, state: FSMContext):
    await message.answer("Выберите целевой формат", reply_markup=keyboards.get_formats_kb())
    await MyFSM.waiting_format.set()


async def return_converted_file(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            output_filepath = do_convert(input_filepath=data['input_filepath'], target_format=message.text)
        except Exception as e:
            await message.answer(e)
            await send_welcome(message=message, state=state)
            raise Exception
    await state.finish()
    with UploadFile(output_filepath) as file:
        await message.answer_document(file)


async def send_err_incorrect_frmt(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, пришлите изображение как файл')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(asking_file, commands=['convert'], state='*')
    dp.register_message_handler(taking_file, state=MyFSM.waiting_file, content_types='any')
    dp.register_message_handler(return_converted_file, state=MyFSM.waiting_format)


