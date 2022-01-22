from apy.services import Services
from utilities.eumn_token_symbols import TokenSymbols


class TokenUtilities:
    def get_token_price_in_eth(reward_token_ticker, token_ticker):

        try:
            services = Services(token=reward_token_ticker, token_ticker=token_ticker)
            data = services.token_price()
            token_in_usdt = float(data["price"])
        except Exception as e:
            token_in_usdt = 1.0

        try:
            services = Services(TokenSymbols.ETH.value, token_ticker=token_ticker)
            data = services.token_price()
            eth_in_usdt = float(data["price"])
        except Exception as e:
            raise Exception(e)

        return token_in_usdt / eth_in_usdt
