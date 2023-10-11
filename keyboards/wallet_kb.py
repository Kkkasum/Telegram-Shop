from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


btn1_wallet = InlineKeyboardButton(text='Card', callback_data='card_payment')
btn2_wallet = InlineKeyboardButton(text='Crypto', callback_data='crypto_payment')
btn3_wallet = InlineKeyboardButton(text='⬅ Вернуться', callback_data='profile')

wallet_keyboard = InlineKeyboardMarkup().row(
    btn1_wallet,
    btn2_wallet
).add(btn3_wallet)
