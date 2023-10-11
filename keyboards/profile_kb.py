from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


btn1_profile = InlineKeyboardButton(text='💰 Пополнить', callback_data='wallet')
btn2_profile = InlineKeyboardButton(text='🛒 Мои покупки', callback_data='my_purchases')

profile_keyboard = InlineKeyboardMarkup().row(
    btn1_profile,
    btn2_profile
)