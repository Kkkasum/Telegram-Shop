from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.database import get_order_by_id, get_user, get_user_orders_ids
from src.keyboards import (
    OrderCallbackFactory,
    OrdersHistoryCallbackFactory,
    ProfileCallbackFactory,
    create_orders_history_kb,
    create_profile_kb,
    create_refill_methods_kb,
    create_return_history_kb,
)
from src.utils import messages as msg
from src.utils.formatters import format_order, format_profile

router = Router()


@router.callback_query(ProfileCallbackFactory.filter())
async def callback_profile(callback: types.CallbackQuery, callback_data: ProfileCallbackFactory, state: FSMContext):
    if callback_data.page == 'profile':
        await state.clear()
        user = await get_user(callback.from_user.id)
        profile_kb = create_profile_kb()
        m = format_profile(
            callback.from_user.username,
            callback.from_user.id,
            user['registration_date'],
            user['balance']
        )
        await callback.message.edit_text(text=m, reply_markup=profile_kb)

    if callback_data.page == 'refill':
        refill_methods_kb = create_refill_methods_kb()
        await callback.message.edit_text(text=msg.refill_methods_msg, reply_markup=refill_methods_kb)


@router.callback_query(OrdersHistoryCallbackFactory.filter())
async def callback_orders_history(callback: types.CallbackQuery, callback_data: OrdersHistoryCallbackFactory):
    orders_ids = await get_user_orders_ids(user_id=callback.from_user.id)

    if not orders_ids:
        await callback.answer(text=msg.no_purchases_msg, show_alert=True)
    else:
        orders_start, orders_stop = (callback_data.page - 1) * 5, callback_data.page * 5
        total = len(orders_ids) // 5 + len(orders_ids) % 5

        orders_history_kb = create_orders_history_kb(orders_ids[orders_start:orders_stop], total, callback_data.page)
        await callback.message.edit_text(text=msg.orders_history_msg)
        await callback.message.edit_reply_markup(reply_markup=orders_history_kb)


@router.callback_query(OrderCallbackFactory.filter())
async def callback_order(callback: types.CallbackQuery, callback_data: OrderCallbackFactory):
    if callback_data.action == 'show':
        order = await get_order_by_id(callback_data.order_id)
        m = format_order(callback_data.order_id, order['item_name'], order['order_date'])
        return_kb = create_return_history_kb()

        await callback.message.edit_text(text=m)
        await callback.message.edit_reply_markup(reply_markup=return_kb)
