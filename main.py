from data.config import BOT_TOKEN, PAYMASTER_TOKEN, CRYPTO_PAY_TOKEN, DB_PATH, review_chat
from states import MainStates, PaymentStates
from functions.get_currencies import get_currencies, currency
from functions.cryptobot_pay import get_crypto_bot_sum, check_crypto_bot_invoice

from db.db import BotDB

import logging
import datetime

from keyboards.main_kb import main_keyboard
from keyboards.profile_kb import profile_keyboard
from keyboards.wallet_kb import wallet_keyboard
from keyboards.crypto_kb import check_crypto_kb

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import ContentType
from aiogram.utils.markdown import hlink

from aiocryptopay import AioCryptoPay


# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = BotDB(db_file=DB_PATH)


# start
@dp.message_handler(Command('start'))
async def start(message: types.Message):
    m = f"🌕 Добро пожаловать, {message.from_user.first_name} \n\n" \
        f"🌖 Бот работает в штатном режиме \n" \
        f"🌗 Если не появились вспомогательные кнопки \n" \
        f"🌘 Введите /start \n\n" \
        f"🌑 <a href='{review_chat}'>Отзывы покупателей</a>"

    if not db.user_exists(message.from_user.id):
        registration_date = datetime.datetime.now().strftime('%d/%m/%Y')

        user = {
            'unique_id': message.from_user.id,  # int
            'username': message.from_user.username,  # str
            'registration_date': registration_date,  # str
            'balance': 0  # float
        }

        db.add_user(user=user)

    await message.answer(text=m, reply_markup=main_keyboard, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


# profile
@dp.message_handler(state=MainStates.profile)
@dp.message_handler(Text(equals='Профиль', ignore_case=True))
async def profile(message: types.Message, state: FSMContext):
    await MainStates.profile.set()

    user = db.get_user_info(message.from_user.id)

    m = f"👤 <b>Логин:</b> @{message.from_user.username}\n" \
        f"🕑 <b>Регистрация:</b> {user['registration_date']}\n" \
        f"🔑 <b>ID:</b> {user['unique_id']}\n\n" \
        f"💲 <b>Баланс:</b> {user['balance']}"

    await storage.set_bucket(chat=message.chat.id, user=message.from_user.id, bucket=user)

    await message.answer(text=m, reply_markup=profile_keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


# help
@dp.message_handler(state=MainStates.help)
@dp.message_handler(Text(equals='Помощь', ignore_case=True))
async def help(message: types.Message, state: FSMContext):
    await MainStates.help.set()

    m = f"❗ Правила:\n\n" \
        f"<b>1.</b> Пользователь согласен, что время обработки заявки занимает до 1 рабочего дня.\n\n" \
        f"<b>1.1</b> Флуд, мат, оскорбления, невежливое общение, введение в заблуждение, обман - причины ограничения " \
        f"поддержки/доступа к боту без дальнейшей помощи в разбирательстве вашей проблемы.\n\n" \
        f"<b>1.2</b> Фиксируйте покупку на видео. Начинайте запись видео до того как нажали на кнопку \"купить\", не \ " \
        f"завершая запись продолжайте проверку товара, если есть такая возможность.  При невалидности товара замена " \
        f"выдаётся при наличии пруфов в течение 30 минут после покупки.\n\n" \
        f"<b>1.3</b> Возврат средств происходит только на баланс бота.\n\n" \
        f"<b>1.4</b> В случае, если способ получения фиксят и товар не выдан -  осуществляется возврат. " \
        f"Если товар выдан и был отобран самой компанией - возврат не осуществляется\n\n" \
        f"<b>1.5</b> Приобретая товар, вы обязуетесь воспользоваться услугой в течение 24ч"

    await message.answer(text=m, reply_markup=main_keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


# catalog
@dp.message_handler(state=MainStates.catalog)
@dp.message_handler(Text(equals='Каталог', ignore_case=True))
async def catalog(message: types.Message, state: FSMContext):
    await MainStates.catalog.set()

    categories = db.get_categories()

    await storage.set_bucket(chat=message.chat.id, bucket=categories)

    btns = [InlineKeyboardButton(text=k, callback_data=k.lower()) for k in categories]
    catalog_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(*btns)

    await message.answer(text='Выберите категорию:', reply_markup=catalog_keyboard)
    await state.finish()


# callbacks handler
@dp.callback_query_handler(lambda c: True)
async def callbacks_handler(call: types.CallbackQuery, state: FSMContext, callback_data: dict = None):
    # profile
    if call.data == 'profile':
        user = await storage.get_bucket(chat=call.message.chat.id, user=call.from_user.id)
        if user and 'registration_date' in user:

            m = f"👤 <b>Логин:</b> @{call.from_user.username}\n" \
                f"🕑 <b>Регистрация:</b> {user['registration_date']}\n" \
                f"🔑 <b>ID:</b> {user['unique_id']}\n\n" \
                f"💲 <b>Баланс:</b> {user['balance']}"
        else:
            user = db.get_user_info(call.from_user.id)

            m = f"👤 <b>Логин:</b> @{call.from_user.username}\n"\
                f"🕑 <b>Регистрация:</b> {user['registration_date']}\n"\
                f"🔑 <b>ID:</b> {user['unique_id']}\n\n" \
                f"💲 <b>Баланс:</b> {user['balance']}"

        await call.message.edit_text(text=m, reply_markup=profile_keyboard, parse_mode=ParseMode.HTML)

    # user's purchases history
    if call.data == 'my_purchases':
        await state.finish()

        purchases_history = [f"🕑 Дата покупки: {i[0]}\n"
                             f"🛒 Товар: {i[1]}\n"
                             f"💰 Цена: {i[2]}\n\n"
                             for i in db.get_purchaces_history(call.from_user.id)]

        if not purchases_history:
            error_m = '❗ У вас отсутствуют покупки'
            await call.answer(text=error_m, show_alert=True)
            # await state.finish()
        else:
            await call.message.answer(text=''.join(purchases_history))
            # await state.finish()

    # catalog
    # # item's categories
    if call.data == 'catalog':
        await state.finish()
        categories = db.get_categories()

        btns = [InlineKeyboardButton(text=k, callback_data=k.lower()) for k in categories]
        catalog_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)\
            .add(*btns)

        await call.message.edit_text(text='Выберите категорию:', reply_markup=catalog_keyboard)

    # # items by category
    categories = {k.lower(): v for k, v in db.get_categories().items()}

    if call.data in categories:
        category_id = categories[call.data]
        items = db.get_items_by_category(category_id)

        btns = [InlineKeyboardButton(text=f"{item['name']} | {item['price']} руб. | {item['amount']} шт.",
                                     callback_data=item['name'])
                for item in items]
        btn_return = InlineKeyboardButton(text='⬅ Вернуться', callback_data='catalog')
        items_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)\
                            .add(*btns)\
                            .add(btn_return)

        await storage.set_bucket(chat=call.message.chat.id,
                                 user=call.from_user.id,
                                 bucket={item['name']: item for item in items})

        await call.message.edit_text(text='Выберите товар:', reply_markup=items_keyboard)

    # # item's choosing
    items = await storage.get_bucket(chat=call.message.chat.id, user=call.from_user.id)

    if call.data in items:
        item = items[call.data]

        m = f"<b>Покупка товара</b>\n\n"\
            f"<b>Название:</b> {item['name']}\n"\
            f"<b>Категория:</b> {item['category']}\n"\
            f"<b>Стоимость:</b> {item['price']}\n\n"\
            f"<b>Описание:</b> \n{item['description']}\n\n"\
            f"<b>Если у вас остались вопросы касательно товара, свяжитесь с поддержкой</b> @nuiktotvoyidol"

        await storage.set_bucket(chat=call.message.chat.id, user=call.from_user.id, bucket=item)

        btn_buy = InlineKeyboardButton(text='💰 Купить товар', callback_data='buy_item')
        btn_return = InlineKeyboardButton(text='⬅ Вернуться', callback_data=item['category'].lower())
        item_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)\
            .add(btn_buy)\
            .add(btn_return)

        await call.message.edit_text(text=m, reply_markup=item_keyboard, parse_mode=ParseMode.HTML)

    # # item's purchase confirm
    if call.data == 'buy_item':
        item_data = await storage.get_bucket(chat=call.message.chat.id, user=call.from_user.id)

        m = f"<b>Вы действительно хотите купить этот товар?</b>\n\n"\
            f"<b>🛒 Товар</b>: {item_data['name']}\n"\
            f"<b>💰 Сумма к оплате:</b> {item_data['price']}"

        btn_confirm = InlineKeyboardButton(text='✅ Подтвердить', callback_data='buying_confirmed')
        btn_cancel = InlineKeyboardButton(text='❌ Отменить', callback_data='catalog')
        buy_item_keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True).row(
            btn_confirm,
            btn_cancel
        )

        await call.message.edit_text(text=m, reply_markup=buy_item_keyboard, parse_mode=ParseMode.HTML)

    # # buying confirmed
    if call.data == 'buying_confirmed':
        user = db.get_user_info(unique_id=call.from_user.id)
        item = await storage.get_bucket(chat=call.message.chat.id, user=call.from_user.id)

        confirmed_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)

        if user['balance'] > item['price']:
            order_date = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')

            # update db
            order = {
                'type': 'item purchase',
                'unique_id': call.from_user.id,
                'item_name': item['name'],
                'order_date': order_date,
                'price': item['price']
            }
            new_balance = user['balance'] - item['price']
            new_amount = item['amount'] - 1

            db.add_order(order=order) # adding order
            db.update(
                table='users',
                column='balance',
                value=new_balance if new_balance > 0 else 0,
                where_column='unique_id',
                row=call.from_user.id
            )  # updating user's balance after purchase
            db.update(
                table='items',
                column='item_amount',
                value=new_amount if new_amount > 0 else 0,
                where_column='item_name',
                row=item['name']
            )  # updating item's amount after purchase

            m = f"✅ <b>Покупка произошла успешно</b>\n\n"\
                f"<b>Товар:</b> {item['name']}\n"\
                f"<b>Сумма покупки:</b> {item['price']}\n"\
                f"<b>Покупатель:</b> @{call.from_user.username} ({call.from_user.id})\n"\
                f"<b>Дата покупки:</b> {order_date}"

            await call.message.edit_text(text=m, parse_mode=ParseMode.HTML)
        else:
            confirmed_keyboard.add(InlineKeyboardButton(text='💰 Пополнить', callback_data='wallet'))
            m = f"❗ <b>У вас недостаточно средств на счету</b>"

            await call.message.edit_text(text=m, reply_markup=confirmed_keyboard, parse_mode=ParseMode.HTML)

    # payments
    btn_return = InlineKeyboardButton(text='⬅ Вернуться', callback_data='wallet')

    if call.data == 'wallet':
        m = f"💰 Выберите способ пополнения"

        user = db.get_user_info(call.from_user.id)
        await storage.set_bucket(chat=call.message.chat.id, user=call.from_user.id, bucket=user)

        await call.message.edit_text(text=m, reply_markup=wallet_keyboard)
        await state.finish()

    if call.data == 'card_payment':
        m = f"💰 Введите сумму пополнения"

        await call.message.edit_text(text=m)
        await PaymentStates.card.set()

    if call.data == 'crypto_payment':
        m = f"💰 Введите сумму пополнения (от 100 руб.)"

        await call.message.edit_text(text=m)
        await PaymentStates.crypto.set()

    if call.data.startswith('crypto_transaction_'):
        amount, asset = call.data[19:].split()

        cryptopay = AioCryptoPay(CRYPTO_PAY_TOKEN)
        invoice = await cryptopay.create_invoice(
            asset=asset,
            amount=amount
        )
        await cryptopay.close()

        m = f"<b>Для пополнения баланса перейдите {hlink('по ссылке', invoice.pay_url)} и оплатите счет</b>\n\n" \
            f"После оплаты нажмите на <b>Проверить оплату</b>"

        await call.message.delete()
        await call.message.answer(text=m,
                                  reply_markup=check_crypto_kb(invoice.pay_url, invoice.invoice_id).add(btn_return),
                                  parse_mode=ParseMode.HTML)

    if call.data.startswith('check_crypto_bot'):
        if await check_crypto_bot_invoice(token=CRYPTO_PAY_TOKEN, invoice_id=int(call.data.split('|')[1])):
            m = f"✅ Оплата прошла успешно"
            user = await storage.get_bucket(chat=call.message.chat.id, user=call.message.from_user.id)

            order_date = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            amount = await state.get_data()['amount_of_money']
            new_balance = user['balance'] + amount

            order = {
                'type': 'refill wallet',
                'unique_id': call.message.from_user.id,
                'item_name': 'Wallet',
                'order_date': order_date,
                'price': await state.get_data()['amount_of_money']
            }
            db.add_order(order=order)
            db.update(table='users',
                      column='balance',
                      value=new_balance,
                      where_column='unique_id',
                      row=call.message.from_user.id)

            await call.answer(text=m, show_alert=True)
        else:
            m = f"❗ Вы не оплатили счет"

            await call.answer(text=m, show_alert=True)


# card
@dp.message_handler(state=PaymentStates.card)
async def card(message: types.Message, state: FSMContext):
    error_m = f"❌ Данные были введены неверно. \n" \
              f"💰 Введите сумму для пополнения средств"

    btn_return = InlineKeyboardButton('⬅ Вернуться', callback_data='wallet')
    card_keyboard = InlineKeyboardMarkup().add(btn_return)

    if message.text.isdigit():
        await state.update_data(amount_of_money=message.text)
        amount = int((await state.get_data())['amount_of_money']) * 100
        prices = types.LabeledPrice(label='Refill Wallet', amount=amount)
        await bot.send_invoice(chat_id=message.chat.id,
                               title='Refill Wallet',
                               description=f"Refill Wallet: {prices['amount'] / 100}",
                               provider_token=PAYMASTER_TOKEN,
                               currency='rub',
                               payload='test-invoice-card',
                               prices=[prices])
        await state.finish()
    else:
        if message.text == 'Каталог':
            await state.finish()
            await catalog(message, state)
        elif message.text == 'Помощь':
            await state.finish()
            await help(message, state)
        elif message.text == 'Профиль':
            await state.finish()
            await profile(message, state)
        else:
            await message.answer(text=error_m, reply_markup=card_keyboard)


# pre checkout
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)


# successful payment by card
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    m = f"✅ Пополнение на сумму " \
        f"{message.successful_payment.total_amount // 100} " \
        f"{message.successful_payment.currency} " \
        f"прошло успешно."

    payment_info = message.successful_payment.to_python()

    user = await storage.get_bucket(chat=message.chat.id, user=message.from_user.id)
    new_balance = user['balance'] + payment_info['total_amount'] / 100

    order_date = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    order = {
        'type': 'refill wallet',
        'unique_id': message.from_user.id,
        'item_name': 'Wallet',
        'order_date': order_date,
        'price': payment_info['total_amount'] / 100
    }

    db.add_order(order=order)
    db.update(table='users',
              column='balance',
              value=new_balance,
              where_column='unique_id',
              row=message.from_user.id)

    await message.answer(text=m)


# crypto
@dp.message_handler(state=PaymentStates.crypto)
async def crypto(message: types.Message, state: FSMContext):
    m = "💲 Сумма пополнения: {amount}\n\n" \
        "💰 <b>Выберите валюту пополнения</b>"

    error_m = f"❌ Данные были введены неверно.\n" \
              f"💰 Введите сумму для пополнения средств"

    crypto_keyboard = InlineKeyboardMarkup()
    btn_return = InlineKeyboardButton('⬅ Вернуться', callback_data='wallet')

    if message.text.isdigit():
        await state.update_data(amount_of_money=message.text)
        amount = (await state.get_data())['amount_of_money']
        currencies = ['USDT', 'BUSD', 'USDC', 'BTC', 'ETH', 'TON', 'BNB']
        currencies_rates = await get_crypto_bot_sum(token=CRYPTO_PAY_TOKEN, amount=int(amount), currencies=currencies)
        currencies_amounts_str = ["{0:15.8f} {1:>2}".format(v, k) for k, v in currencies_rates.items()]
        [crypto_keyboard.add(InlineKeyboardButton(k, callback_data=f"crypto_transaction_{k}"))
         for k in currencies_amounts_str]
        crypto_keyboard.add(btn_return)
        await message.answer(text=m.format(amount=amount), reply_markup=crypto_keyboard, parse_mode=ParseMode.HTML)
        await state.finish()
    else:
        if message.text == 'Каталог':
            await state.finish()
            await catalog(message, state)
        elif message.text == 'Помощь':
            await state.finish()
            await help(message, state)
        elif message.text == 'Профиль':
            await state.finish()
            await profile(message, state)
        else:
            crypto_keyboard.add(btn_return)
            await message.answer(text=error_m, reply_markup=crypto_keyboard)


# run long-polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
    db.close()
