from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src import messages as msg
from src.common import bot, config
from src.states import PaymentStates
from src.keyboards import (
    PaymentCallbackFactory,
    create_return_kb
)


router = Router()


@router.callback_query(PaymentCallbackFactory.filter())
async def callback_payment(callback: types.CallbackQuery, callback_data: PaymentCallbackFactory, state: FSMContext):
    if callback_data.page == 'card_payment':
        await callback.message.edit_text(text=msg.card_payment_msg)
        await state.set_state(PaymentStates.card)

    if callback_data.page == 'crypto_payment':
        await callback.message.edit_text(text=msg.crypto_payment_msg)
        await state.set_state(PaymentStates.crypto)


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
    else:
        back_kb = create_return_kb('profile')
        await message.answer(text=msg.wrong_refill_value, reply_markup=back_kb)


@router.message(StateFilter(PaymentStates.crypto))
async def pay_with_crypto(message: types.Message, tate: FSMContext):
    pass
