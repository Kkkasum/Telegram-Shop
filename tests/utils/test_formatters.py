from datetime import datetime

from src.utils.formatters import (
    format_buying_item,
    format_cancelled_purchase,
    format_crypto_invoice,
    format_item,
    format_order,
    format_profile,
    format_start,
    format_succeed_payment,
    format_succeed_purchase,
)


def test_format_start() -> None:
    res = format_start(
        username='User'
    )

    assert res == '🌕 Добро пожаловать, User\n\n' \
                  '🌖 Бот работает в штатном режиме\n' \
                  '🌗 Если не появились вспомогательные кнопки\n' \
                  '🌘 Введите /start\n\n'


def test_format_profile() -> None:
    res = format_profile(
        username='User',
        user_id=1,
        registration_date=datetime(day=1, month=1, year=2023),
        balance=0
    )

    assert res == '👤 <b>Логин:</b> @User\n'\
                  '🔑 <b>ID:</b> 1\n'\
                  '🕑 <b>Регистрация:</b> 01/01/2023\n\n'\
                  '💲 <b>Баланс:</b> 0.0'


def test_format_succeed_payment() -> None:
    res = format_succeed_payment(
        deposit=1000,
        currency='RUB'
    )

    assert res == '✅ Пополнение на сумму 1000.00 RUB прошло успешно'


def test_format_item() -> None:
    res = format_item(
        name='Item',
        price=100,
        description='Item description'
    )

    assert res == '<b>Покупка товара</b>\n\n'\
                  '<b>Название:</b> Item\n'\
                  '<b>Стоимость:</b> 100\n\n'\
                  '<b>Описание:</b> \nItem description'


def test_format_buying_item() -> None:
    res = format_buying_item(
        item_name='Item',
        price=100
    )

    assert res == '<b>Вы действительно хотите купить этот товар?</b>\n\n' \
                  '<b>🛒 Товар</b>: Item\n' \
                  '<b>💰 Сумма к оплате:</b> 100'


def test_format_order() -> None:
    res = format_order(
        order_id=1,
        item_name='Item',
        order_date=datetime(day=1, month=1, year=2023)
    )

    assert res == '<b>Номер заказа:</b> 1\n'\
                  'Товар: Item\n'\
                  'Дата покупки: 01/01/2023'\



def test_format_crypto_invoice() -> None:
    res = format_crypto_invoice(
        invoice_url='url'
    )

    assert res == 'Для пополнения баланса перейдите по <a href="url">ссылке</a>\n'\
                  'После оплаты нажмите на кнопку <b>Проверить оплату</b>'


def test_format_succeed_purchase() -> None:
    res = format_succeed_purchase(
        item_name='Item',
        price=100,
        username='User',
        user_id=1
    )

    assert res == '✅ <b>Покупка прошла успешно</b>\n\n' \
                  '<b>Товар:</b> Item\n' \
                  '<b>Сумма покупки:</b> 100\n' \
                  '<b>Покупатель:</b> @User (1)'


def test_format_cancelled_purchase() -> None:
    res = format_cancelled_purchase(
        user_balance=100
    )

    assert res == '❗ <b>У вас недостаточно средств на счету</b>\n' \
                  'Ваш баланс: 100'
