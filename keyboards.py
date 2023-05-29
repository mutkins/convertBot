from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton


def get_formats_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('jpg')
    kb.add(button)
    button = KeyboardButton('png')
    kb.add(button)
    button = KeyboardButton('/отмена')
    kb.add(button)
    return kb