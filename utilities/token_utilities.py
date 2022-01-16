from apy.services import Services


class TokenUtilities:
    def get_token_price_in_eth(token_ticker):

        try:
            services = Services(token=token_ticker)
            data = services.token_price()
            token_in_usdt = float(data["price"])
        except Exception as e:
            token_in_usdt = 1.0

        try:
            services = Services('ETH')
            data = services.token_price()
            eth_in_usdt = float(data["price"])
        except Exception as e:
            raise Exception(e)

        return token_in_usdt / eth_in_usdt
