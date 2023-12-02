from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


wallet_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Card', callback_data='card_payment'),
            InlineKeyboardButton(text='Crypto', callback_data='crypto_payment')
        ],
        [
            InlineKeyboardButton(text='⬅ Вернуться', callback_data='profile')
        ]
    ]
)
