from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database import get_categories, get_items_by_category


class MenuCallbackFactory(CallbackData, prefix='menu'):
    action: str
    page: str


class ProfileCallbackFactory(CallbackData, prefix='profile'):
    action: str
    page: str


class PaymentCallbackFactory(CallbackData, prefix='payment'):
    action: str
    page: str


class ItemCallbackFactory(CallbackData, prefix='payment'):
    action: str
    page: str
    item_name: str
    price: float


class CategoriesCallbackFactory(CallbackData, prefix='category'):
    action: str
    id: int


class ItemsCallbackFactory(CallbackData, prefix='item'):
    action: str
    id: int


def create_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='💰 Пополнить', callback_data=ProfileCallbackFactory(action='show', page='refill'))
    builder.button(text='🛒 Мои покупки', callback_data=ProfileCallbackFactory(action='show', page='purchases'))
    builder.adjust(2)

    return builder.as_markup()


def create_return_kb(page: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='⬅️ Вернуться', callback_data=MenuCallbackFactory(action='return', page=page))

    return builder.as_markup()


def create_buy_kb(item_name: str, price: float) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='💰 Купить товар',
        callback_data=ItemCallbackFactory(action='buy', page='buy_item', item_name=item_name, price=price)
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MenuCallbackFactory(action='return', page='catalog')
    )

    return builder.as_markup()


def create_purchase_kb(item_name: str, price: float) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='✅ Подтвердить',
        callback_data=ItemCallbackFactory(action='confirm', page='confirm', item_name=item_name, price=price)
    )
    builder.button(
        text='❌ Отменить',
        callback_data=MenuCallbackFactory(action='cancel', page='catalog')
    )

    return builder.as_markup()


def create_cancelled_purchase_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='💰 Пополнить баланс',
        callback_data=ProfileCallbackFactory(action='show', page='refill')
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MenuCallbackFactory(action='cancel', page='catalog')
    )

    return builder.as_markup()


async def create_categories_kb() -> InlineKeyboardMarkup:
    categories = await get_categories()

    builder = InlineKeyboardBuilder()
    [
        builder.button(text=category[1], callback_data=CategoriesCallbackFactory(action='show', id=category[0]))
        for category in categories
    ]
    builder.adjust(1)

    return builder.as_markup()


async def create_items_kb(category_id: int) -> InlineKeyboardMarkup:
    items = await get_items_by_category(category_id)

    builder = InlineKeyboardBuilder()
    [
        builder.button(text=item[1], callback_data=ItemsCallbackFactory(action='show', id=item[0]))
        for item in items
    ]
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MenuCallbackFactory(action='return', page='catalog')
    )
    builder.adjust(1)

    return builder.as_markup()


def create_refill_methods_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Карта',
        callback_data=PaymentCallbackFactory(action='refill', page='card_payment')
    )
    builder.button(
        text='Криптовалюта',
        callback_data=PaymentCallbackFactory(action='refill', page='crypto_payment')
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=MenuCallbackFactory(action='return', page='profile')
    )
    builder.adjust(1)

    return builder.as_markup()
