from datetime import datetime, timezone

from aiogram import Router, types

from src import messages as msg
from src.database import get_user, get_item_by_id, add_order
from src.keyboards import (
    CategoriesCallbackFactory,
    ItemsCallbackFactory,
    ItemCallbackFactory,
    create_items_kb,
    create_buy_kb,
    create_purchase_kb,
    create_cancelled_purchase_kb
)


router = Router()


@router.callback_query(CategoriesCallbackFactory.filter())
async def callback_category(callback: types.CallbackQuery, callback_data: CategoriesCallbackFactory):
    items_kb = await create_items_kb(int(callback_data.id))

    await callback.message.edit_text(text=msg.items_msg, reply_markup=items_kb)


@router.callback_query(ItemsCallbackFactory.filter())
async def callback_item(callback: types.CallbackQuery, callback_data: ItemsCallbackFactory):
    item = await get_item_by_id(int(callback_data.id))
    buy_kb = create_buy_kb(item['item_name'], item['price'])
    m = msg.item_msg.format(
        name=item['item_name'],
        price=item['price'],
        description=item['description']
    )

    await callback.message.edit_text(text=m, reply_markup=buy_kb)


@router.callback_query(ItemCallbackFactory.filter())
async def callback_payment(callback: types.CallbackQuery, callback_data: ItemCallbackFactory):
    if callback_data.page == 'buy_item':
        purchase_kb = create_purchase_kb(callback_data.item_name, callback_data.price)
        m = msg.buy_item_msg.format(
            item_name=callback_data.item_name,
            price=callback_data.price
        )

        await callback.message.edit_text(text=m, reply_markup=purchase_kb)

    if callback_data.page == 'confirm':
        user = await get_user(callback.from_user.id)

        if user['balance'] < callback_data.price:
            cancelled_purchase_kb = create_cancelled_purchase_kb()

            await callback.message.edit_text(text=msg.cancelled_purchase_msg, reply_markup=cancelled_purchase_kb)
        else:
            order = {
                'order_type': 'purchase',
                'user_id': callback.from_user.id,
                'item_name': callback_data.item_name,
                'order_date': datetime.now(tz=timezone.tzname('Europe/Moscow')),
                'price': callback_data.price
            }
            m = msg.succeed_purchase_msg.format(
                item_name=order['item_name'],
                price=order['price'],
                username=callback.from_user.username,
                user_id=callback.from_user.id,
                order_date=order['order_date']
            )

            await callback.message.edit_text(text=m)
            await add_order(order)
