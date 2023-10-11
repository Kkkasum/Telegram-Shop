from aiocryptopay import AioCryptoPay


async def get_crypto_bot_sum(token: str, amount: float, currencies: list) -> dict:
    crypto = AioCryptoPay(token=token)
    courses = await crypto.get_exchange_rates()
    await crypto.close()

    currencies_rates = {course.source: amount / course.rate
                        for course in courses
                        if course.source in currencies and course.target == 'RUB'}
    return currencies_rates


async def check_crypto_bot_invoice(token: str, invoice_id: int) -> bool:
    cryptopay = AioCryptoPay(token)
    invoice = await cryptopay.get_invoices(invoice_ids=invoice_id)
    await cryptopay.close()
    if invoice.status == 'paid':
        return True
    else:
        return False
