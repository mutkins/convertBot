from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton
from settings import IMAGE_FORMATS, VIDEO_FORMATS


def get_formats_kb(convert_type):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if convert_type == 'vid':
        for item in VIDEO_FORMATS:
            button = KeyboardButton(item)
            kb.add(button)
    elif convert_type == 'img':
        for item in IMAGE_FORMATS:
            button = KeyboardButton(item)
            kb.add(button)
    return kb
