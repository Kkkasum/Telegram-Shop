from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


class ProfileCallbackFactory(CallbackData, prefix='profile'):
    action: str
    page: str


def create_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='💰 Пополнить', callback_data=ProfileCallbackFactory(action='show', page='refill'))
    builder.button(text='🛒 Мои покупки', callback_data=ProfileCallbackFactory(action='show', page='purchases'))
    builder.adjust(2)

    return builder.as_markup()


def create_return_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='⬅️ Вернуться', callback_data=ProfileCallbackFactory(action='return', page='profile'))

    return builder.as_markup()
