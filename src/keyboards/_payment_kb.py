from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from ._profile_kb import ProfileCallbackFactory


class PaymentCallbackFactory(CallbackData, prefix='payment'):
    action: str
    page: str


def create_refill_methods_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Карта',
        callback_data=PaymentCallbackFactory(action='refill', page='card_payment')
    )
    builder.button(
        text='Криптовалюта (недоступно)',
        callback_data=PaymentCallbackFactory(action='refill', page='crypto_payment')
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=ProfileCallbackFactory(action='return', page='profile')
    )
    builder.adjust(1)

    return builder.as_markup()
