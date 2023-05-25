from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton


def get_welcome_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('/каталог')
    kb.add(button)
    button = KeyboardButton('/мои_рецепты')
    kb.add(button)
    return kb


def get_formats_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton('jpg')
    kb.add(button)
    button = KeyboardButton('png')
    kb.add(button)
    button = KeyboardButton('/отмена')
    kb.add(button)
    return kb