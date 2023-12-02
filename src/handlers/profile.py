from aiogram import Router, types

from src.database import get_user_purchases
from src import messages as msg
from src.keyboards import (
    ProfileCallbackFactory,
    create_refill_methods_kb
)


router = Router()


@router.callback_query(ProfileCallbackFactory.filter())
async def callback_profile(callback: types.CallbackQuery, callback_data: ProfileCallbackFactory):
    if callback_data.page == 'refill':
        refill_methods_kb = create_refill_methods_kb()

        await callback.message.edit_text(text=msg.refill_methods_msg, reply_markup=refill_methods_kb)

    if callback.data == 'purchases':
        purchases = await get_user_purchases(callback.from_user.id)

        if not purchases:
            await callback.answer(text=msg.no_purchases_msg, show_alert=True)
        else:
            m = [
                msg.purchases_msg.format(
                    order_date=purchase[0],
                    item_name=purchase[1],
                    price=purchase[2]
                )
                for purchase in purchases
            ]
            await callback.answer(text=''.join(m))
