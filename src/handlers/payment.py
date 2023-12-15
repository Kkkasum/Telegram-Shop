from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types.message import ContentType

from sqlalchemy import func

from loguru import logger

from src.utils import messages as msg
from src.utils.formatters import format_crypto_invoice, format_succeed_payment
from src.utils.crypto_pay import create_invoice as create_crypto_invoice, check_invoice as check_crypto_invoice
from src.common import bot, config
from src.states import PaymentStates
from src.database import add_order, update_user_balance, get_user_balance
from src.keyboards import (
    PaymentCallbackFactory,
    AssetCallbackFactory,
    InvoiceCallbackFactory,
    create_return_profile_kb,
    create_rates_kb,
    create_crypto_invoice_kb
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
async def card_invoice(message: types.Message, state: FSMContext):
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

        logger.success(f'Card invoice to {message.from_user.id} has been sent')
    else:
        back_kb = create_return_profile_kb()
        await message.answer(text=msg.wrong_value_msg, reply_markup=back_kb)


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    deposit = message.successful_payment.total_amount / 100
    user_balance = await get_user_balance(message.from_user.id)
    user_balance += deposit
    m = format_succeed_payment(deposit, message.successful_payment.currency)

    await message.answer(text=m)
    await add_order({
        'order_type': 'refill',
        'user_id': message.from_user.id,
        'item_name': 'Balance',
        'order_date': func.now(),
        'price': deposit
    })
    await update_user_balance(message.from_user.id, user_balance)

    logger.success(f'User {message.from_user.id} deposited balance for {deposit} by card')


@router.message(StateFilter(PaymentStates.crypto))
async def pay_with_crypto(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        deposit = int(message.text)
        rates_kb = await create_rates_kb(deposit)

        await message.answer(text=msg.asset_pay_msg, reply_markup=rates_kb)
        await state.clear()
    else:
        back_kb = create_return_profile_kb()
        await message.answer(text=msg.wrong_value_msg, reply_markup=back_kb)


@router.callback_query(AssetCallbackFactory.filter())
async def crypto_assets(callback: types.CallbackQuery, callback_data: AssetCallbackFactory):
    if callback_data.action == 'invoice':
        invoice = await create_crypto_invoice(callback_data.asset, callback_data.deposit)
        crypto_invoice_kb = create_crypto_invoice_kb(invoice.bot_invoice_url, invoice.invoice_id, callback_data.deposit)
        m = format_crypto_invoice(invoice.bot_invoice_url)

        await callback.message.edit_text(text=m, reply_markup=crypto_invoice_kb)


@router.callback_query(InvoiceCallbackFactory.filter())
async def crypto_invoice(callback: types.CallbackQuery, callback_data: InvoiceCallbackFactory):
    if await check_crypto_invoice(callback_data.invoice_id):
        user_balance = await get_user_balance(callback.from_user.id)
        user_balance += callback_data.deposit
        m = format_succeed_payment(callback_data.deposit)

        await callback.message.answer(text=m)
        await add_order({
            'order_type': 'refill',
            'user_id': callback.from_user.id,
            'item_name': 'Balance',
            'order_date': func.now(),
            'price': callback_data.deposit
        })
        await update_user_balance(callback.from_user.id, user_balance)

        logger.success(f'User {callback.from_user.id} deposited balance for {callback_data.deposit} by crypto')
    else:
        await callback.message.answer(text=msg.not_paid_invoice_msg)
