import asyncio

from states import PaymentStates
# from functions.cryptobot_pay import get_crypto_bot_sum, check_crypto_bot_invoice

from src.common import bot, dp
from src.handlers import menu_router, profile_router, payment_router, catalog_router


async def main():
    dp.include_router(menu_router)
    dp.include_router(profile_router)
    dp.include_router(payment_router)
    dp.include_router(catalog_router)

    await dp.start_polling(bot)


# callbacks handler
# @dp.callback_query_handler(lambda c: True)
# async def callbacks_handler(call: types.CallbackQuery, state: FSMContext, callback_data: dict = None):
#     # payments
#     btn_return = InlineKeyboardButton(text='⬅ Вернуться', callback_data='wallet')
#
#     if call.data == 'wallet':
#         m = f"💰 Выберите способ пополнения"
#
#         user = db.get_user_info(call.from_user.id)
#         await storage.set_bucket(chat=call.message.chat.id, user=call.from_user.id, bucket=user)
#
#         await call.message.edit_text(text=m, reply_markup=wallet_kb)
#         await state.finish()
#
#     if call.data == 'card_payment':
#         m = f"💰 Введите сумму пополнения"
#
#         await call.message.edit_text(text=m)
#         await PaymentStates.card.set()
#
#     if call.data == 'crypto_payment':
#         m = f"💰 Введите сумму пополнения (от 100 руб.)"
#
#         await call.message.edit_text(text=m)
#         await PaymentStates.crypto.set()
#
#     if call.data.startswith('crypto_transaction_'):
#         amount, asset = call.data[19:].split()
#
#         cryptopay = AioCryptoPay(CRYPTO_PAY_TOKEN)
#         invoice = await cryptopay.create_invoice(
#             asset=asset,
#             amount=amount
#         )
#         await cryptopay.close()
#
#         m = f"<b>Для пополнения баланса перейдите {hlink('по ссылке', invoice.pay_url)} и оплатите счет</b>\n\n" \
#             f"После оплаты нажмите на <b>Проверить оплату</b>"
#
#         await call.message.delete()
#         await call.message.answer(text=m,
#                                   reply_markup=check_crypto_kb(invoice.pay_url, invoice.invoice_id).add(btn_return),
#                                   parse_mode=ParseMode.HTML)
#
#     if call.data.startswith('check_crypto_bot'):
#         if await check_crypto_bot_invoice(token=CRYPTO_PAY_TOKEN, invoice_id=int(call.data.split('|')[1])):
#             m = f"✅ Оплата прошла успешно"
#             user = await storage.get_bucket(chat=call.message.chat.id, user=call.message.from_user.id)
#
#             order_date = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')
#             amount = await state.get_data()['amount_of_money']
#             new_balance = user['balance'] + amount
#
#             order = {
#                 'type': 'refill wallet',
#                 'unique_id': call.message.from_user.id,
#                 'item_name': 'Wallet',
#                 'order_date': order_date,
#                 'price': await state.get_data()['amount_of_money']
#             }
#             db.add_order(order=order)
#             db.update(table='users',
#                       column='balance',
#                       value=new_balance,
#                       where_column='unique_id',
#                       row=call.message.from_user.id)
#
#             await call.answer(text=m, show_alert=True)
#         else:
#             m = f"❗ Вы не оплатили счет"
#
#             await call.answer(text=m, show_alert=True)
#
#
# # card
# @dp.message_handler(state=PaymentStates.card)
# async def card(message: types.Message, state: FSMContext):
#     error_m = f"❌ Данные были введены неверно. \n" \
#               f"💰 Введите сумму для пополнения средств"
#
#     btn_return = InlineKeyboardButton('⬅ Вернуться', callback_data='wallet')
#     card_kb = InlineKeyboardMarkup().add(btn_return)
#
#     if message.text.isdigit():
#         await state.update_data(amount_of_money=message.text)
#         amount = int((await state.get_data())['amount_of_money']) * 100
#         prices = types.LabeledPrice(label='Refill Wallet', amount=amount)
#         await bot.send_invoice(chat_id=message.chat.id,
#                                title='Refill Wallet',
#                                description=f"Refill Wallet: {prices['amount'] / 100}",
#                                provider_token=PAYMASTER_TOKEN,
#                                currency='rub',
#                                payload='test-invoice-card',
#                                prices=[prices])
#         await state.finish()
#     else:
#         if message.text == 'Каталог':
#             await state.finish()
#             await catalog(message, state)
#         elif message.text == 'Помощь':
#             await state.finish()
#             await help(message, state)
#         elif message.text == 'Профиль':
#             await state.finish()
#             await profile(message, state)
#         else:
#             await message.answer(text=error_m, reply_markup=card_kb)
#
#
# # pre checkout
# @dp.pre_checkout_query_handler(lambda query: True)
# async def pre_checkout_query(q: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(q.id, ok=True)
#
#
# # successful payment by card
# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
# async def successful_payment(message: types.Message):
#     m = f"✅ Пополнение на сумму " \
#         f"{message.successful_payment.total_amount // 100} " \
#         f"{message.successful_payment.currency} " \
#         f"прошло успешно."
#
#     payment_info = message.successful_payment.to_python()
#
#     user = await storage.get_bucket(chat=message.chat.id, user=message.from_user.id)
#     new_balance = user['balance'] + payment_info['total_amount'] / 100
#
#     order_date = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')
#     order = {
#         'type': 'refill wallet',
#         'unique_id': message.from_user.id,
#         'item_name': 'Wallet',
#         'order_date': order_date,
#         'price': payment_info['total_amount'] / 100
#     }
#
#     db.add_order(order=order)
#     db.update(table='users',
#               column='balance',
#               value=new_balance,
#               where_column='unique_id',
#               row=message.from_user.id)
#
#     await message.answer(text=m)
#
#
# # crypto
# @dp.message_handler(state=PaymentStates.crypto)
# async def crypto(message: types.Message, state: FSMContext):
#     m = "💲 Сумма пополнения: {amount}\n\n" \
#         "💰 <b>Выберите валюту пополнения</b>"
#
#     error_m = f"❌ Данные были введены неверно.\n" \
#               f"💰 Введите сумму для пополнения средств"
#
#     crypto_kb = InlineKeyboardMarkup()
#     btn_return = InlineKeyboardButton('⬅ Вернуться', callback_data='wallet')
#
#     if message.text.isdigit():
#         await state.update_data(amount_of_money=message.text)
#         amount = (await state.get_data())['amount_of_money']
#         currencies = ['USDT', 'BUSD', 'USDC', 'BTC', 'ETH', 'TON', 'BNB']
#         currencies_rates = await get_crypto_bot_sum(token=CRYPTO_PAY_TOKEN, amount=int(amount), currencies=currencies)
#         currencies_amounts_str = ["{0:15.8f} {1:>2}".format(v, k) for k, v in currencies_rates.items()]
#         [crypto_kb.add(InlineKeyboardButton(k, callback_data=f"crypto_transaction_{k}"))
#          for k in currencies_amounts_str]
#         crypto_kb.add(btn_return)
#         await message.answer(text=m.format(amount=amount), reply_markup=crypto_kb, parse_mode=ParseMode.HTML)
#         await state.finish()
#     else:
#         if message.text == 'Каталог':
#             await state.finish()
#             await catalog(message, state)
#         elif message.text == 'Помощь':
#             await state.finish()
#             await help(message, state)
#         elif message.text == 'Профиль':
#             await state.finish()
#             await profile(message, state)
#         else:
#             crypto_kb.add(btn_return)
#             await message.answer(text=error_m, reply_markup=crypto_kb)
#

# run long-polling
if __name__ == '__main__':
    asyncio.run(main())
