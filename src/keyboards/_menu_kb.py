from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


menu_kb = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Каталог')
        ],
        [
            KeyboardButton(text='Помощь')
        ],
        [
            KeyboardButton(text='Профиль')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Выберите действие из меню'
)
