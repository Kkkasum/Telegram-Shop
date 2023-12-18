from datetime import datetime


def format_start(username: str) -> str:
    start_msg = f"🌕 Добро пожаловать, {username}\n\n" \
                f"🌖 Бот работает в штатном режиме\n" \
                f"🌗 Если не появились вспомогательные кнопки\n" \
                f"🌘 Введите /start\n\n"

    return start_msg


def format_profile(username: str, user_id: int, registration_date: datetime, balance: float) -> str:
    profile_msg = f"👤 <b>Логин:</b> @{username}\n" \
                  f"🔑 <b>ID:</b> {user_id}\n" \
                  f"🕑 <b>Регистрация:</b> {registration_date.strftime('%d/%m/%Y')}\n\n" \
                  f"💲 <b>Баланс:</b> {balance}"

    return profile_msg


def format_order(order_id: int, item_name: str, order_date: datetime) -> str:
    order_msg = f"<b>Номер заказа:</b> {order_id}\n"\
                f"Товар: {item_name}\n"\
                f"Дата покупки: {order_date.strftime('%d/%m/%Y')}"\

    return order_msg


def format_crypto_invoice(invoice_url: str) -> str:
    crypto_invoice_msg = f'Для пополнения баланса перейдите по <a href="{invoice_url}">ссылке</a>\n'\
                         f'После оплаты нажмите на <b>Проверить оплату</b>'

    return crypto_invoice_msg


def format_succeed_payment(deposit: float, currency: str = 'RUB') -> str:
    successful_payment_msg = f"✅ Пополнение на сумму {deposit} {currency} прошло успешно"

    return successful_payment_msg


def format_item(name: str, price: float, description: str) -> str:
    item_msg = f"<b>Покупка товара</b>\n\n" \
               f"<b>Название:</b> {name}\n" \
               f"<b>Стоимость:</b> {price}\n\n" \
               f"<b>Описание:</b> \n{description}"

    return item_msg


def format_buying_item(item_name: str, price: float) -> str:
    buying_item_msg = f"<b>Вы действительно хотите купить этот товар?</b>\n\n" \
                      f"<b>🛒 Товар</b>: {item_name}\n" \
                      f"<b>💰 Сумма к оплате:</b> {price}"

    return buying_item_msg


def format_succeed_purchase(item_name: str, price: float, username: str, user_id: int) -> str:
    succeed_purchase_msg = f"✅ <b>Покупка прошла успешно</b>\n\n" \
                           f"<b>Товар:</b> {item_name}\n" \
                           f"<b>Сумма покупки:</b> {price}\n" \
                           f"<b>Покупатель:</b> @{username} ({user_id})"

    return succeed_purchase_msg


def format_cancelled_purchase(user_balance: float) -> str:
    cancelled_purchase_msg = f"❗ <b>У вас недостаточно средств на счету</b>\n" \
                             f"Ваш баланс: {user_balance}"

    return cancelled_purchase_msg
