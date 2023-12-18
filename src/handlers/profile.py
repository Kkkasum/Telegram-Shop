from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.database import get_user, get_user_purchases, get_order_by_id
from src.utils import messages as msg
from src.utils.formatters import format_profile, format_purchases
from src.keyboards import (
    ProfileCallbackFactory,
    OrdersHistoryCallbackFactory,
    OrderCallbackFactory,
    create_profile_kb,
    create_refill_methods_kb,
    create_orders_history_kb
)


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
async def callback_history(callback: types.CallbackQuery, callback_data: OrdersHistoryCallbackFactory):
    if callback_data.action == 'history':
        purchases = await get_user_purchases(user_id=callback.from_user.id, limit=callback_data.page)

        if not purchases:
            await callback.answer(text=msg.no_purchases_msg, show_alert=True)
        else:
            await callback.message.edit_reply_markup()


@router.callback_query(OrderCallbackFactory.filter())
async def callback_order(callback: types.CallbackQuery, callback_data: OrderCallbackFactory):
    if callback_data.action == 'item':
        order = await get_order_by_id(callback_data.order_id)

