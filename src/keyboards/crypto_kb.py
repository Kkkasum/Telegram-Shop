from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def check_crypto_kb(url: str, invoice_hash: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='🔗 Оплатить',
                        url=url
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='♻ Проверить оплату',
                        callback_data=f'check_crypto_bot|{invoice_hash}'
                    )
                ]
            ]
        )

    return markup
