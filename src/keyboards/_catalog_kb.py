from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from ._payment_kb import PaymentCallbackFactory
from src.database import get_categories, get_items_by_category


class CatalogCallbackFactory(CallbackData, prefix='catalog'):
    action: str
    page: str


class ItemsCallbackFactory(CallbackData, prefix='item'):
    action: str
    id: int


class ItemCallbackFactory(CallbackData, prefix='payment'):
    action: str
    page: str
    item_name: str
    price: float


async def create_categories_kb() -> InlineKeyboardMarkup:
    categories = await get_categories()

    builder = InlineKeyboardBuilder()
    [
        builder.button(text=category[1], callback_data=CatalogCallbackFactory(action=str(category[0]), page='category'))
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
        callback_data=CatalogCallbackFactory(action='return', page='catalog')
    )
    builder.adjust(1)

    return builder.as_markup()


def create_buy_kb(item_name: str, price: float) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='💰 Купить товар',
        callback_data=ItemCallbackFactory(action='buy', page='buy_item', item_name=item_name, price=price)
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=CatalogCallbackFactory(action='show', page='catalog')
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
        callback_data=CatalogCallbackFactory(action='show', page='catalog')
    )

    return builder.as_markup()


def create_cancelled_purchase_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='💰 Пополнить баланс',
        callback_data=PaymentCallbackFactory(action='show', page='refill')
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=CatalogCallbackFactory(action='cancel', page='catalog')
    )

    return builder.as_markup()
