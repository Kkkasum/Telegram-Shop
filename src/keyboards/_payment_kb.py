from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from ._profile_kb import ProfileCallbackFactory


class PaymentCallbackFactory(CallbackData, prefix='payment'):
    action: str
    page: str


class AssetCallbackFactory(CallbackData, prefix='asset'):
    action: str
    asset: str
    deposit: float


class InvoiceCallbackFactory(CallbackData, prefix='invoice'):
    action: str
    invoice_id: int
    deposit: float


def create_refill_methods_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Карта',
        callback_data=PaymentCallbackFactory(action='refill', page='card_payment')
    )
    builder.button(
        text='Криптовалюта',
        callback_data=PaymentCallbackFactory(action='refill', page='crypto_payment')
    )
    builder.button(
        text='⬅️ Вернуться',
        callback_data=ProfileCallbackFactory(action='return', page='profile')
    )
    builder.adjust(1)

    return builder.as_markup()


def create_rates_kb(rates: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    [
        builder.button(
            text=f'{rate:.4f} {asset}',
            callback_data=AssetCallbackFactory(action='invoice', asset=asset, deposit=rate)
        )
        for asset, rate in rates.items()
    ]
    builder.button(
        text='⬅️ Вернуться',
        callback_data=ProfileCallbackFactory(action='return', page='profile')
    )
    builder.adjust(1)

    return builder.as_markup()


def create_crypto_invoice_kb(invoice_url: str, invoice_id: int, deposit: float) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Оплатить',
        url=invoice_url
    )
    builder.button(
        text='Проверить оплату',
        callback_data=InvoiceCallbackFactory(action='check', invoice_id=invoice_id, deposit=deposit)
    )
    builder.adjust(1)

    return builder.as_markup()
