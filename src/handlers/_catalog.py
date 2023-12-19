from aiogram import Router, types
from sqlalchemy import func

from src.database import add_order, get_categories, get_item_by_id, get_items_by_category, get_user, update_user_balance
from src.keyboards import (
    CatalogCallbackFactory,
    ItemCallbackFactory,
    ItemsCallbackFactory,
    create_buy_kb,
    create_cancelled_purchase_kb,
    create_categories_kb,
    create_items_kb,
    create_purchase_kb,
)
from src.utils import messages as msg
from src.utils.formatters import format_buying_item, format_cancelled_purchase, format_item, format_succeed_purchase

router = Router()


@router.callback_query(CatalogCallbackFactory.filter())
async def callback_catalog(callback: types.CallbackQuery, callback_data: CatalogCallbackFactory):
    if callback_data.page == 'catalog':
        categories = await get_categories()
        categories_kb = create_categories_kb(categories)
        await callback.message.edit_text(text=msg.catalog_msg, reply_markup=categories_kb)

    if callback_data.page == 'category':
        items = await get_items_by_category(int(callback_data.action))
        items_kb = create_items_kb(items)
        await callback.message.edit_text(text=msg.items_msg, reply_markup=items_kb)


@router.callback_query(ItemsCallbackFactory.filter())
async def callback_items(callback: types.CallbackQuery, callback_data: ItemsCallbackFactory):
    item = await get_item_by_id(int(callback_data.id))
    buy_kb = create_buy_kb(item['item_name'], item['price'])
    m = format_item(item['item_name'], item['price'], item['description'])

    await callback.message.edit_text(text=m, reply_markup=buy_kb)


@router.callback_query(ItemCallbackFactory.filter())
async def callback_item(callback: types.CallbackQuery, callback_data: ItemCallbackFactory):
    if callback_data.page == 'buy_item':
        purchase_kb = create_purchase_kb(callback_data.item_name, callback_data.price)
        m = format_buying_item(callback_data.item_name, callback_data.price)

        await callback.message.edit_text(text=m, reply_markup=purchase_kb)

    if callback_data.page == 'confirm':
        user = await get_user(callback.from_user.id)

        if user['balance'] < callback_data.price:
            cancelled_purchase_kb = create_cancelled_purchase_kb()
            m = format_cancelled_purchase(user['balance'])

            await callback.message.edit_text(text=m, reply_markup=cancelled_purchase_kb)
        else:
            user_balance = user['balance'] - callback_data.price
            order = {
                'order_type': 'purchase',
                'user_id': callback.from_user.id,
                'item_name': callback_data.item_name,
                'order_date': func.now(),
                'price': callback_data.price
            }
            m = format_succeed_purchase(
                order['item_name'],
                order['price'],
                callback.from_user.username,
                callback.from_user.id
            )

            await callback.message.edit_text(text=m)
            await add_order(order)
            await update_user_balance(callback.from_user.id, user_balance)
