from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


btn1_main = KeyboardButton(text='Каталог')
btn2_main = KeyboardButton(text='Помощь')
btn3_main = KeyboardButton(text='Профиль')

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(btn1_main)\
    .add(btn2_main)\
    .add(btn3_main)
