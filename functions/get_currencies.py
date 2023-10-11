import cryptocompare


fiat = 'RUB'
currency = ['USDT', 'BUSD', 'USDC', 'BTC', 'ETH', 'TON', 'BNB']


def get_currencies() -> list:
    interest = 1.03

    cur = [cryptocompare.get_price(fiat, i)[fiat] for i in currency]
    currencies_rate = [i[j] * interest for i, j in zip(cur, currency)]

    return currencies_rate
