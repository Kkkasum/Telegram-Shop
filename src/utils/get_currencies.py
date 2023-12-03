import cryptocompare


def get_currencies() -> list:
    interest = 1.03
    tokens = ['USDT', 'BUSD', 'USDC', 'BTC', 'ETH', 'TON']

    rates = [cryptocompare.get_price('RUB', i)['RUB'] for i in tokens]
    tokens_rate = [i[j] * interest for i, j in zip(rates, tokens)]

    return tokens_rate
