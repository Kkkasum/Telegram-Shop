from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.invoice import Invoice

from src.common import config

crypto = AioCryptoPay(token=config.CRYPTO_BOT_TOKEN, network=Networks.TEST_NET)


async def get_crypto_rates(deposit: int) -> dict:
    assets = ['ETH', 'TON', 'LTC', 'USDT', 'USDC']

    rates = {}
    for asset in assets:
        rate = await crypto.get_amount_by_fiat(
            summ=deposit,
            asset=asset,
            target='RUB'
        )
        rates[asset] = rate

    return rates


async def create_invoice(asset: str, deposit: float) -> Invoice:
    invoice = await crypto.create_invoice(deposit, asset, expires_in=6000)

    return invoice


async def check_invoice(invoice_id: int) -> bool:
    invoice = await crypto.get_invoices(invoice_ids=invoice_id)
    if invoice.status == 'paid':
        return True
    else:
        return False
