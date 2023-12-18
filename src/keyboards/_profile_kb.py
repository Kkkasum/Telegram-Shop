from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ProfileCallbackFactory(CallbackData, prefix='profile'):
    action: str
    page: str


class OrdersHistoryCallbackFactory(CallbackData, prefix='purchases'):
    action: str
    page: int


class OrderCallbackFactory(CallbackData, prefix='order'):
    action: str
    order_id: int


def create_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='💰 Пополнить', callback_data=ProfileCallbackFactory(action='show', page='refill'))
    builder.button(text='🛒 Мои покупки', callback_data=OrdersHistoryCallbackFactory(action='history', page=1))
    builder.adjust(2)

    return builder.as_markup()


def create_return_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='⬅️ Вернуться', callback_data=ProfileCallbackFactory(action='return', page='profile'))

    return builder.as_markup()


def create_orders_history_kb(orders_ids: list[int], total: int, page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    [
        builder.button(
            text=f'Заказ #{order_id}',
            callback_data=OrderCallbackFactory(action='show', order_id=order_id)
        )
        for order_id in orders_ids
    ]
    if page == 1:
        builder.button(text='⬅️', callback_data=ProfileCallbackFactory(action='return', page='profile'))
    else:
        builder.button(text='⬅️', callback_data=OrdersHistoryCallbackFactory(action='show', page=page - 1))
    builder.button(
        text=f'{page}/{total}',
        callback_data=OrdersHistoryCallbackFactory(action='show', page=page)
    )
    builder.button(text='➡️', callback_data=OrdersHistoryCallbackFactory(action='show', page=page + 1))

    sizes = [1 for _ in range(len(orders_ids))]
    sizes.append(3)

    builder.adjust(*sizes)

    return builder.as_markup()


def create_return_history_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='⬅️ Вернуться', callback_data=OrdersHistoryCallbackFactory(action='return', page=1))

    return builder.as_markup()
