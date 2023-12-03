from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types.message import ContentType

from sqlalchemy import func

from loguru import logger

from src import messages as msg
from src.common import bot, config
from src.states import PaymentStates
from src.database import add_order, update_user_balance, get_user_balance
from src.keyboards import (
    PaymentCallbackFactory,
    create_return_profile_kb
)


router = Router()


@router.callback_query(PaymentCallbackFactory.filter())
async def callback_payment(callback: types.CallbackQuery, callback_data: PaymentCallbackFactory, state: FSMContext):
    if callback_data.page == 'card_payment':
        await callback.message.edit_text(text=msg.card_payment_msg)
        await state.set_state(PaymentStates.card)

    if callback_data.page == 'crypto_payment':
        await callback.message.edit_text(text='Недоступно')


@router.message(StateFilter(PaymentStates.card))
async def pay_with_card(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        deposit = int(message.text)
        prices = types.LabeledPrice(label='Пополнение баланса', amount=deposit * 100)

        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Пополнение баланса',
            description=f'Пополнение баланса на сумму: {deposit}',
            provider_token=config.PAYMASTER_TOKEN,
            currency='rub',
            payload='test-invoice-card',
            prices=[prices]
        )
        await state.clear()

        logger.success(f"Invoice to {message.from_user.id} has been sent")
    else:
        back_kb = create_return_profile_kb()
        await message.answer(text=msg.wrong_refill_value, reply_markup=back_kb)


# @router.message(StateFilter(PaymentStates.crypto))
# async def pay_with_crypto(message: types.Message, state: FSMContext):
#     if message.text.isdigit():
#         deposit = int(message.text)
#     else:
#         back_kb = create_return_profile_kb()
#         await message.answer(text=msg.wrong_refill_value, reply_markup=back_kb)


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    deposit = message.successful_payment.total_amount / 100
    user_balance = await get_user_balance(message.from_user.id)
    user_balance += deposit
    m = msg.successful_payment.format(
        deposit=deposit,
        currency=message.successful_payment.currency
    )

    await message.answer(text=m)
    await add_order({
        'order_type': 'refill',
        'user_id': message.from_user.id,
        'item_name': 'Balance',
        'order_date': func.now(),
        'price': deposit
    })
    await update_user_balance(message.from_user.id, user_balance)
